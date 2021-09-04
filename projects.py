
import database


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

    return tempProjects * 6
