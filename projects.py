
import database


def getAllProjectsForPath(diskPath):
    tempProjects = []
    tempProject = database.StetsonProj()
    tempProject['DATE_CREATED'] = "2018.01.18_16:52:41"
    tempProject['DATE_MODIFIED'] = "2021.08.13_15:29:58"
    tempProject['DESCRIPTION'] = "Amazon Alexa skill for augmented play with foam-based weaponry."
    tempProject['DIRECTORY_NAS'] = "/mnt/y/home/2018_01_18_alexaDartBattle"
    tempProject['FILE_TYPES'] = ["py", "png", "md", "txt", "mp3", "mp4", "prproj", "cfa", "pek", "log", "csv"]
    tempProject['GIT_ENABLED'] = True
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
    tempProject['THUMBNAIL_WSL'] = "/mnt/y/home/2018_01_18_alexaDartBattle/media/dartBattleLogo_108x108.png"
    tempProject['THUMBNAIL'] = "icons/project_dartbattle.png"
    tempProject['USER_CONTRIBUTORS'] = ["allen", "jisun", "owen"]
    tempProject['USER_CREATED'] = "allen"
    tempProject['USER_MODIFIED'] = "jisun"
    tempProjects.append(tempProject)
    return tempProjects * 6
