
import datetime
import os

from PyQt5 import QtGui, QtWidgets

import projects

USING_SAMPLE_DATA = True


def getAllCategories():
    # TODO: implement me
    return sorted(["home", "church", "school"])


def getAllProjects():
    return projects.getAllProjectsForPath("/mnt/y")


def getAllProjectTypes():
    # TODO: implement me
    return sorted(["music", "video", "alexa"])


def getAllTags():
    # TODO: implement me
    allTags = []
    allTags.extend(getAllCategories())
    allTags.extend(getAllProjectTypes())
    allTags.extend(["nerf", "demoreel", "alexa", "arduino", "nas", "music",
                    "bass", "st. kilian", "bathgate", "violin", "ethan"])
    return sorted(set(allTags))

def getCategoryFromProject(project):
    if not "PROJECT_CATEGORY" in project:
        return ""
    return project["PROJECT_CATEGORY"]


def getContributorsFromProject(project, icons=True):
    if not "USER_CONTRIBUTORS" in project:
        return []
    contributors = []
    for contributor in sorted(project["USER_CONTRIBUTORS"]):
        if not icons:
            contributors.append(contributor.lower())
            continue
        pixmap = None
        if USING_SAMPLE_DATA:
            imagePath = "samples/{}.png".format(contributor.lower())
            if not os.path.exists("./" + imagePath):
                pixmap = QtGui.QPixmap("icons/user.png")
            pixmap = QtGui.QPixmap(imagePath)
        else:
            pixmap = database.getImageForUser(contributor.lower())
        if pixmap:
            pixmap = pixmap.scaledToHeight(25)
            contributors.append(pixmap)
    return contributors


def getDateCreatedFromProject(project):
    if not "DATE_CREATED" in project:
        return "-"
    return project["DATE_CREATED"].split("_")[0]

def getDateModifiedFromProject(project):
    if not "DATE_MODIFIED" in project:
        return "-"
    return project["DATE_MODIFIED"].split("_")[0]

def getDescriptionFromProject(project):
    if not "DESCRIPTION" in project:
        return "-"
    return project["DESCRIPTION"]


def getFileTypesFromProject(project):
    if not "FILE_TYPES" in project:
        return ""
    returnTypes = ""
    for fileType in project["FILE_TYPES"]:
        # we don't want anything past # of characters
        if len(returnTypes) > 50:
            returnTypes += ", ..."
            break
        if not returnTypes:
            returnTypes = fileType
        else:
            returnTypes += ", " + fileType
    return returnTypes


def getIconForUser(userName):
    if USING_SAMPLE_DATA:
        imagePath = "samples/{}.png".format(userName)
        if not os.path.exists("./" + imagePath):
            icon = QtGui.QIcon("icons/user.png")
        else:
            icon = QtGui.QIcon(imagePath)
        return icon
    else:
        # Get this from the database
        pass

def getIntegrationsFromProject(project):
    if not "INTEGRATIONS" in project:
        return []
    returnIntegrations = []
    integrations = project["INTEGRATIONS"]
    for integration in integrations:
        iconPath = "icons/{}.png".format(integration)
        if not os.path.exists("./" + iconPath):
            iconPath = "icons/user.png"
        integPix = QtGui.QPixmap(iconPath)
        integPix = integPix.scaledToHeight(20)
        returnIntegrations.append(integPix)
    return returnIntegrations


def getNotesPreviewFromProject(project):
    if not "NOTES" in project:
        return ["-"]
    notesReturn = []
    allDates = sorted(project["NOTES"].keys(), reverse=True)
    for i, noteDateStr in enumerate(allDates):
        # we only have room for 2 lines on notes.
        if i > 1:
            break
        noteDate = datetime.datetime.strptime(noteDateStr, "%Y.%m.%d_%H:%M:%S")
        prettyDate = noteDate.strftime("(%Y.%m.%d) ")
        # limit the entry to the first 90 characters
        noteEntry = project["NOTES"][noteDateStr]
        if len(noteEntry) > 90:
            noteEntry = noteEntry[:87] + "..."
        notesReturn.append(prettyDate + noteEntry)
    return notesReturn

def getProjectStatusFromProject(project):
    if not "PROJECT_STATUS" in project:
        return ""
    return project["PROJECT_STATUS"]


def getProjectTypeFromProject(project):
    if not "PROJECT_TYPE" in project:
        return ""
    return project["PROJECT_TYPE"]


def getTagsFromProject(project, extraTags=False):
    tags = project["TAGS"]
    if extraTags:
        tags.append(getProjectTypeFromProject(project))
        tags.append(getCategoryFromProject(project))
    return tags


def getTitleFromProject(project):
    return project["PROJECT_NAME"]


def getThumbnailFromProject(project):
    if not "THUMBNAIL_PATH" in project:
        return None
    if USING_SAMPLE_DATA:
        thumbPath = project["THUMBNAIL_PATH"]
        if not thumbPath or not os.path.exists(thumbPath):
            thumbPath = "icons/project_unknown.png"
        pixmap = QtGui.QPixmap(thumbPath)
    else:
        pixmap = project["THUMBNAIL_PATH"]
    pixmap = pixmap.scaledToHeight(80)
    return pixmap


def getUserCreatedFromProject(project, icon=True):
    if not "USER_CREATED" in project:
        return None
    if not icon:
        return project["USER_CREATED"].lower()
    if USING_SAMPLE_DATA:
        iconPath = "samples/{}.png".format(project["USER_CREATED"])
        if not os.path.exists("./" + iconPath):
            iconPath = "samples/user.png"
        userCreated = QtGui.QPixmap(iconPath)
    else:
        userCreated = database.getImageForUser(project["USER_CREATED"])
    userCreated = userCreated.scaledToHeight(25)
    return userCreated


def getUserModifiedFromProject(project):
    if not "USER_MODIFIED" in project:
        return None
    if USING_SAMPLE_DATA:
        iconPath = "samples/{}.png".format(project["USER_MODIFIED"])
        if not os.path.exists("./" + iconPath):
            iconPath = "samples/user.png"
        userModified = QtGui.QPixmap(iconPath)
    else:
        userModified = database.getImageForUser(project["USER_CREATED"])
    userModified = userModified.scaledToHeight(25)
    return userModified


def getAllUsersCreated():
    #Pull this from the DB eventually
    return ["allen", "asher", "jisun", "jonah", "owen"]


def getAllUsersModified():
    #Pull this from the DB eventually
    return ["allen", "asher", "jisun", "jonah", "owen"]

def registerProjectBrowserFilter(filterObject):
    widgets = QtWidgets.QApplication.instance().allWidgets()
    for widget in widgets:
        if "__main__.SHPMProjectBrowser" ==  str(widget.__class__).split("'")[1]:
            widget.registerFilter(filterObject)
            break
