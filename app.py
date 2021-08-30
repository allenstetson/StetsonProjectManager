
# std imports
import sys

# qt imports
from PyQt5 import QtCore, QtGui, QtWidgets

# local imports
import controller


class StetsonHPMMainWindow(QtWidgets.QMainWindow):
    """Main window for Stetson HPM"""
    def __init__(self, parent=None):
        super(StetsonHPMMainWindow, self).__init__(parent=parent)
        self.setWindowTitle("Stetson HPM")
        #app.setWindowIcon()
        self.setMinimumSize(QtCore.QSize(500, 350))
        self.resize(QtCore.QSize(1020, 768))
        self.setCentralWidget(StetsonHPMMainWidget(self))


class StetsonHPMMainWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(StetsonHPMMainWidget, self).__init__(parent=parent)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.buildLayout()
        self.setLayout(self.mainLayout)

    def buildLayout(self):
        self.topBar = SHPMTopBar()
        self.mainLayout.addWidget(self.topBar)

        windowStack = SHPMWindowStack(self)
        self.mainLayout.addWidget(windowStack)


class SHPMTopBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(SHPMTopBar, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(
            400,
            10,
            QtWidgets.QSizePolicy.Expanding
            )
        self.layout.addItem(spacer)

        self.profilePicture = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("icons/allen.png")
        self.profilePicture.setPixmap(
            pixmap.scaledToHeight(50)
            )
        self.layout.addWidget(self.profilePicture)
        self.setStyleSheet("background: #CCCCCC;")
        self.setLayout(self.layout)


class SHPMWindowStack(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(SHPMWindowStack, self).__init__(parent=parent)
        self.widget1 = SHPMProjectBrowser()
        self.widget2 = SHPMProjectInspector()
        self.addWidget(self.widget1)
        self.addWidget(self.widget2)


class SHPMProjectBrowser(QtWidgets.QFrame):
    def  __init__(self, parent=None):
        super(SHPMProjectBrowser, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.browserSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.browserSplitter.addWidget(SHPMProjectBrowserFilter(parent=self))
        self.browserSplitter.addWidget(SHPMProjectBrowserList(parent=self))
        self.layout.addWidget(self.browserSplitter)
        self.setLayout(self.layout)


class SHPMProjectBrowserFilter(QtWidgets.QFrame):
    def  __init__(self, parent=None, *args, **kwargs):
        super(SHPMProjectBrowserFilter, self).__init__(parent=parent, *args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        mylabel = QtWidgets.QLabel("Browser Filter")
        self.layout.addWidget(mylabel)
        self.setLayout(self.layout)
        self.setMaximumWidth(200)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)


class SHPMProjectBrowserDelegate(QtWidgets.QItemDelegate):
    """
    def  __init__(self, parent=None, *args):
        super(SHPMProjectBrowserDelegate, self).__init__(parent=parent, *args)
        print("In the delegate")
    """

    def paint(self, painter, option, index):
        #FIXME: This gets continually called/calculated on mouse move.
        #  Somehow ensure that this happens once, caches, and serves the cache
        painter.save()

        # item background
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.gray))
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        painter.drawRect(option.rect)

        # item
        value = index.data(QtCore.Qt.DisplayRole)
        if not value:
            return

        # Common Fonts
        fontMed10 = QtGui.QFont("Arial", 10, QtGui.QFont.Medium)
        fontMed9 = QtGui.QFont("Arial", 9, QtGui.QFont.Medium)
        fontBold10 = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)
        fontBold20 = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        fontBold30 = QtGui.QFont("Arial", 30, QtGui.QFont.Bold)


        # --------- left --------------
        ## item TN
        if value["THUMBNAIL"]:
            thumb = QtGui.QPixmap(value["THUMBNAIL"])
            topLeft = option.rect.topLeft()
            position = QtCore.QPoint(topLeft.x() + 5, topLeft.y() + 5)
            painter.drawPixmap(position, thumb)

        ## Contributors
        contributors = controller.getContributorsFromProject(value)
        for i, contributor in enumerate(contributors):
            if i > 3:  # we only have room for 4 pix
                break
            topLeft = option.rect.topLeft()
            thisX = topLeft.x() + 5 + (25 * i)
            thisY = topLeft.y() + 125
            position = QtCore.QPoint(thisX, thisY)
            painter.drawPixmap(position, contributor)

        # --------- center ------------
        ## item title
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setFont(fontBold30)
        title = value["PROJECT_NAME"]
        coords = list(option.rect.getCoords())
        # offset coords by thumbnail size; use fixed for now
        coords[0] += 125
        coords[1] += 5
        coords[2] += 125
        coords[3] += 5
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, title)
        ## description
        thisFont = fontMed9
        thisFont.setItalic(True)
        painter.setFont(thisFont)
        descr = value["DESCRIPTION"]
        coords[1] += 40
        coords[3] += 40
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, descr)

        ## item created date
        coords[1] += 15
        coords[3] += 15
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        userCreated = QtGui.QPixmap("icons/allen.png")
        userCreated = userCreated.scaledToHeight(20)
        painter.drawPixmap(upperLeft, userCreated)

        coords[0] += 25
        coords[1] += 5
        coords[2] += 25
        coords[3] += 5
        painter.setFont(fontBold10)
        created = "created: "
        widthOffset = QtGui.QFontMetrics(fontBold10).width(created)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, created)
        #
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(fontMed10)
        created = value["DATE_CREATED"].split("_")[0]
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, created)
        # return painter cursor to left margin
        coords[0] -= (25 + widthOffset)
        coords[2] -= (25 + widthOffset)

        ## item modified date
        coords[1] += 15
        coords[3] += 15
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        userModified = controller.getUserModifiedFromProject(value)
        painter.drawPixmap(upperLeft, userModified)

        coords[0] += 25
        coords[1] += 5
        coords[2] += 25
        coords[3] += 5
        painter.setFont(fontBold10)
        mod = "last modified: "
        widthOffset = QtGui.QFontMetrics(fontBold10).width(mod)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, mod)
        #
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(fontMed10)
        mod = controller.getDateModifiedFromProject(value)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, mod)
        # return painter cursor to left margin
        coords[0] -= (25 + widthOffset)
        coords[2] -= (25 + widthOffset)

        ## Notes
        coords[1] += 20
        coords[3] += 20
        painter.setFont(fontMed10)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, "NOTES:")
        coords[0] += 10
        coords[2] += 10
        painter.setFont(fontMed9)

        for noteStr in controller.getNotesPreviewFromProject(value):
            coords[1] += 15
            coords[3] += 15
            painter.drawText(
                QtCore.QRect(*coords),
                QtCore.Qt.AlignLeft,
                noteStr)
        coords[0] -= 10
        if len(controller.getNotesPreviewFromProject(value)) < 2:
            # We always want to pad like there are two lines of notes:
            coords[1] += 15

        ## file types
        coords[1] += 20
        fileTypeStr = controller.getFileTypesFromProject(value)

        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setFont(fontMed10)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, fileTypeStr)

        # ---------- utility for tagging --------
        def paintTag(tag, color, coords):
            # box
            widthOffset = QtGui.QFontMetrics(fontBold10).width(tag) + 10
            coords[2] = widthOffset
            tagColor = QtGui.QColor(*color)
            painter.setBrush(QtGui.QBrush(tagColor))
            painter.drawRect(QtCore.QRect(*coords))

            # text
            coords[0] += 8  # pad the text in the box
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
            painter.setFont(fontMed9)
            painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, tag)
            # prepare for the next tag:
            coords[0] += widthOffset
            return coords

        # --------- right -------------
        ## category
        coords = list(option.rect.getCoords())
        coords[0] = coords[2] - 100 # The right column is 100 from the edge
        coords[1] += 60  # The first entry is after the descr, 60 down
        coords[3] = 15
        pstatus = controller.getProjectStatusFromProject(value)
        statusColors = {
            "released": (75, 190, 90),
            "in progress": (217, 211, 48),
            "on hold": (200, 152, 60),
            "unknown": (200, 200, 200)
        }
        if pstatus in statusColors:
            pcolor = statusColors[pstatus]
        else:
            pcolor = statusColors["unknown"]
        paintTag(pstatus, pcolor, coords)

        ## git icon
        coords = list(option.rect.getCoords())
        coords[0] = coords[2] - 100
        coords[1] += 80
        if controller.isProjectGitEnabled(value):
            gitIcon = QtGui.QPixmap("icons/git.png")
            gitIcon = gitIcon.scaledToHeight(20)
            position = QtCore.QPoint(coords[0], coords[1])
            painter.drawPixmap(position, gitIcon)

        # --------- bottom ------------
        ## Tags
        coords = list(option.rect.getCoords())

        coords[0] += 5 # pad the width a tag
        coords[1] = coords[3] - 20  # height just off the bottom of the rect
        coords[3] = 15  # height of 15

        category = controller.getCategoryFromProject(value)
        if category:
            coords = paintTag(category, (200, 152, 60), coords)

        ptype = controller.getProjectTypeFromProject(value)
        if ptype:
            coords = paintTag(ptype, (217, 211, 48), coords)

        for tag in controller.getTagsFromProject(value):
            if tag in [category, ptype]:
                # No sense in repeating info, just skip this
                continue
            coords = paintTag(tag, (124, 191, 190), coords)

        



        painter.restore()

    def sizeHint(self, option, index):
        size = QtCore.QSize(200, 200)
        return size


class SHPMProjectBrowserList(QtWidgets.QFrame):
    def  __init__(self, parent=None):
        super(SHPMProjectBrowserList, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        allProjects = controller.getAllProjects()
        self.listModel = SHPMProjectBrowserListModel(allProjects, self)
        self.listDelegate = SHPMProjectBrowserDelegate(self)
        self.listView = QtWidgets.QListView()
        self.listView.setModel(self.listModel)
        self.listView.setItemDelegate(self.listDelegate)
        self.layout.addWidget(self.listView)

        self.setLayout(self.layout)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)


class SHPMProjectBrowserListModel(QtCore.QAbstractListModel):
    def  __init__(self, listData, parent=None):
        super(SHPMProjectBrowserListModel, self).__init__(parent=parent)
        self.listData = listData

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.listData)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listData[index.row()])
        else:
            return QtCore.QVariant()


class SHPMProjectInspector(QtWidgets.QFrame):
    def  __init__(self, parent=None):
        super(SHPMProjectInspector, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        mylabel = QtWidgets.QLabel("Inspector")
        self.layout.addWidget(mylabel)
        self.setLayout(self.layout)



def main():
    app = QtWidgets.QApplication(sys.argv)
    #Splash screen goes here

    mainWindow = StetsonHPMMainWindow()
    mainWindow.show()

    app.exec_()

if __name__ == "__main__":
    main()
