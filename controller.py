
import datetime
import os

from PyQt5 import QtGui

import projects

def getAllProjects():
    return projects.getAllProjectsForPath("/mnt/y")


def getCategoryFromProject(project):
    if not "PROJECT_CATEGORY" in project:
        return ""
    return project["PROJECT_CATEGORY"]


def getContributorsFromProject(project):
    if not "USER_CONTRIBUTORS" in project:
        return []
    contributors = []
    for contributor in sorted(project["USER_CONTRIBUTORS"]):
        imagePath = "icons/{}.png".format(contributor.lower())
        if not os.path.exists("./" + imagePath):
            pass
        pixmap = QtGui.QPixmap(imagePath)
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


def getTagsFromProject(project):
    tags = project["TAGS"]
    return tags


def getThumbnailFromProject(project):
    if not "THUMBNAIL" in project:
        return None
    thumbPath = project["THUMBNAIL"]
    if not os.path.exists(thumbPath):
        thumbPath = "icons/project_unknown.png"
    pixmap = QtGui.QPixmap(thumbPath)
    pixmap = pixmap.scaledToHeight(80)
    return pixmap


def getUserCreatedFromProject(project):
    if not "USER_CREATED" in project:
        return None
    iconPath = "icons/{}.png".format(project["USER_CREATED"])
    if not os.path.exists("./" + iconPath):
        iconPath = "icons/user.png"
    userCreated = QtGui.QPixmap(iconPath)
    userCreated = userCreated.scaledToHeight(25)
    return userCreated


def getUserModifiedFromProject(project):
    if not "USER_MODIFIED" in project:
        return None
    iconPath = "icons/{}.png".format(project["USER_MODIFIED"])
    if not os.path.exists("./" + iconPath):
        iconPath = "icons/user.png"
    userModified = QtGui.QPixmap(iconPath)
    userModified = userModified.scaledToHeight(25)
    return userModified
