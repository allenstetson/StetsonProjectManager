
import os
import multiprocessing
import pathlib
import time

import database


NUM_PROCS = multiprocessing.cpu_count()


def getAllProjectsForPath(diskPath):
    tempProjects = []
    tempProject = database.StetsonProj()
    tempProject['DATE_CREATED'] = "2018.01.18_16:52:41"
    tempProject['DATE_MODIFIED'] = "2021.08.13_15:29:58"
    tempProject['DESCRIPTION'] = "Amazon Alexa skill for augmented play with foam-based weaponry."
    tempProject['DIRECTORY_NAS'] = "/mnt/y/home/2018_01_18_alexaDartBattle"
    tempProject['FILE_TYPES'] = ["py", "png", "md", "txt", "mp3", "mp4", "prproj", "cfa", "pek", "log", "csv"]
    tempProject['INTEGRATIONS'] = ["git", "alexa"]
    tempProject['GIT_ROOT'] = "/mnt/y/home/2018_01_18_alexaDartBattle"
    tempProject['NOTES'] = {
            "2021.08.20_23:23:16": "Now worthy of my public github",
            "2021.08.19_18:44:52": "Cleaned up the intents for battle, wrote docstring for playlists."
    }
    tempProject['OWNER'] = "allen"
    tempProject['PROJECT_CATEGORY'] = "home"
    tempProject['PROJECT_NAME'] = "Dart Battle"
    tempProject['PROJECT_STATUS'] = "released"
    tempProject['PROJECT_TYPE'] = "alexa"
    tempProject['TAGS'] = ["alexa", "nerf", "demoreel"]
    tempProject['THUMBNAIL_PATH_WSL'] = "/mnt/y/home/2018_01_18_alexaDartBattle/media/dartBattleLogo_108x108.png"
    tempProject['THUMBNAIL_PATH'] = "samples/project_dartbattle.png"
    tempProject['THUMBNAIL'] = None
    tempProject['USER_CONTRIBUTORS'] = ["allen", "jisun", "owen"]
    tempProject['USER_CREATED'] = "allen"
    tempProject['USER_MODIFIED'] = "jisun"
    tempProjects.append(tempProject)

    tempProject = database.StetsonProj()
    tempProject['DATE_CREATED'] = "2021.08.29_13:29:18"
    tempProject['DATE_MODIFIED'] = "2021.09.01_22:05:58"
    tempProject['DESCRIPTION'] = "Bass lesson for Patti."
    tempProject['DIRECTORY_NAS'] = "/mnt/y/church/2021_08_29_bassLesson"
    tempProject['FILE_TYPES'] = ["mp4", "prproj"]
    tempProject['INTEGRATIONS'] = []
    tempProject['NOTES'] = {
            "2021.09.1_22:07:16": "Edited and posted",
            "2021.08.29_13:29:52": "Recorded but not edited."
    }
    tempProject['OWNER'] = "allen"
    tempProject['PROJECT_CATEGORY'] = "church"
    tempProject['PROJECT_NAME'] = "Bass Lesson"
    tempProject['PROJECT_STATUS'] = "complete"
    tempProject['PROJECT_TYPE'] = "music"
    tempProject['TAGS'] = ["bass", "st. kilian"]
    tempProject['THUMBNAIL_PATH_WSL'] = ""
    tempProject['THUMBNAIL_PATH'] = ""
    tempProject['THUMBNAIL'] = None
    tempProject['USER_CONTRIBUTORS'] = ["allen"]
    tempProject['USER_CREATED'] = "allen"
    tempProject['USER_MODIFIED'] = "allen"
    tempProjects.append(tempProject)

    tempProject = database.StetsonProj()
    tempProject['DATE_CREATED'] = "2019.12.18_09:22:16"
    tempProject['DATE_MODIFIED'] = "2021.05.15_08:59:32"
    tempProject['DESCRIPTION'] = "Christmas concert for Owen."
    tempProject['DIRECTORY_NAS'] = "/mnt/y/school/owen_2019_christmasMusic"
    tempProject['FILE_TYPES'] = ["mp4", "prproj", "wav", "mov", "jpg"]
    tempProject['INTEGRATIONS'] = []
    tempProject['GIT_ROOT'] = ""
    tempProject['NOTES'] = {
            "2019.12.19_09:25:46": "Edited and posted",
    }
    tempProject['OWNER'] = "allen"
    tempProject['PROJECT_CATEGORY'] = "school"
    tempProject['PROJECT_NAME'] = "Owen 2019 Christmas Concert"
    tempProject['PROJECT_STATUS'] = "released"
    tempProject['PROJECT_TYPE'] = "video"
    tempProject['TAGS'] = ["bathgate", "violin", "ethan"]
    tempProject['THUMBNAIL_PATH_WSL'] = "mnt/y/school/owen_2019_christmasMusic/DSC_0049.JPG"
    tempProject['THUMBNAIL_PATH'] = "samples/project_owen2019concert.png"
    tempProject['THUMBNAIL'] = None
    tempProject['USER_CONTRIBUTORS'] = ["allen", "owen"]
    tempProject['USER_CREATED'] = "allen"
    tempProject['USER_MODIFIED'] = "allen"
    tempProjects.append(tempProject)

    tempProjects.extend(checkDirectoryForUpdates("Y:\\school"))
    #tempProjects.extend(checkDirectoryForUpdates("Y:\\home"))
    #tempProjects.extend(checkDirectoryForUpdates("Y:\\church"))
    #tempProjects.extend(checkDirectoryForUpdates("Y:\\web"))

    return tempProjects

def checkDirectoryForUpdates(dirPath):
    if not os.path.isdir(dirPath):
        msg = "Directory expected. Not a directory: {}".format(dirPath)
        raise ValueError(msg)
    # Get all project roots from all categories
    dirPath = pathlib.Path(dirPath)
    projectRoots = [x for x in dirPath.iterdir() if x.is_dir()]
    projectRootQueue = multiprocessing.Queue()
    for pRoot in projectRoots:
        print("root: {}".format(pRoot))
        projectRootQueue.put(pRoot)
    projectQueue = multiprocessing.Manager().list()
    procs = [
        multiprocessing.Process(
            target=projectPathProcessor,
            args=(projectRootQueue, projectQueue)
        ) for x in range(NUM_PROCS)
    ]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()

    return list(projectQueue)


def projectPathProcessor(projectRootQueue, projectQueue):
    while not projectRootQueue.empty():
        projectRoot = projectRootQueue.get()
        worker = ProjectPathWorker(projectRoot)
        project = worker.run()
        if project:
            projectQueue.append(project)


class ProjectPathWorker(object):
    def __init__(self, projPath):
        self.category = None
        self.contributors = set()
        self.fileTypes = set()
        self.numFiles = 0
        self.owner = None
        self.path = projPath

    def run(self):
        # TODO: Check for a .stetsonproj file with ID
        #  If exists, get the project from the DB and update the properties
        #  If not, then create a new project:
        project = database.StetsonProj()
        project['PROJECT_CATEGORY'] = os.path.split(
            os.path.dirname(self.path))[-1].lower()
        project['DIRECTORY_NAS'] = self.path
        project['PROJECT_NAME'] = os.path.split(self.path)[-1]

        ctime = os.path.getctime(self.path)
        lastMod = None
        modTime = None
        numFiles = 0
        thumbnail = None
        totalSize = 0
        for dirName, dirs, files in os.walk(self.path):
            if ".git" in dirs:
                project['INTEGRATIONS'].append("git")
                project['GIT_ENABLED'] = True
                project['GIT_ROOT'] = dirName
                dirs.remove(".git")
            if ".ask" in dirs:
                project['INTEGRATIONS'].append("alexa")
            # don't include private dirs
            dirs = [x for x in dirs if not x.startswith(".")]
            for fileName in files:
                numFiles += 1
                filePath = os.path.join(dirName, fileName)
                # extensions
                fExt = os.path.splitext(fileName)[1]
                if fExt:
                    self.fileTypes.add(fExt.lower())
                # size
                totalSize += os.stat(filePath).st_size
                # lastMod
                modTime = os.path.getmtime(filePath)
                if not lastMod or modTime < lastMod:
                    lastMod = modTime
                # ctime
                #  Sometimes the main directory is recreated (after a
                #  catastrophy, etc) and the ctime on that dir is not
                #  representative of reality. In that case, just use the
                #  lowest mod time
                if modTime < ctime:
                    ctime = modTime
                # thumbnail
                if not thumbnail and fExt.lower() in [".jpg", ".png", ".jpeg"]:
                    thumbnail = filePath
                    #TODO: Create a circular TN and store in the DB

        project['DATE_CREATED'] = time.ctime(ctime)
        if modTime:
            project["DATE_MODIFIED"] = time.ctime(modTime)
        project["FILE_TYPES"] = list(self.fileTypes)
        project["DISK_USAGE"] = totalSize
        project['NUM_FILES'] = numFiles
        if thumbnail:
            project['THUMBNAIL_PATH'] = thumbnail
        #TODO: Store in the DB
        return project

