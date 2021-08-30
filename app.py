
# std imports
import sys

# qt imports
from PyQt5 import QtCore, QtGui, QtWidgets

# local imports
import controller


TAG_COLORS = {
    "blue":   ((70, 207, 255), (0, 0, 0)),
    "yellow": ((255, 208, 4), (0, 0, 0)),
    "green":  ((0, 227, 101), (0, 0, 0)),
    "grey":   ((238, 238, 238), (0, 0, 0)),
}

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
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        # item background
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawRect(option.rect)

        # item
        value = index.data(QtCore.Qt.DisplayRole)
        if not value:
            return

        framePadding = 25
        thumbnailDimensions = 80

        # Common Fonts
        font10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Normal)
        fontMed10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Medium)
        fontMed9 = QtGui.QFont("Arial", 9, QtGui.QFont.Medium)
        fontMed20 = QtGui.QFont("Roboto", 20, QtGui.QFont.Medium)
        fontBold10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Bold)
        fontBold14 = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
        fontBold20 = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        fontBold25 = QtGui.QFont("Roboto", 25, QtGui.QFont.Bold)
        fontBold30 = QtGui.QFont("Arial", 30, QtGui.QFont.Bold)

        # ---------- utility for tagging --------
        def paintTag(tag, color, coords):
            colorValues = TAG_COLORS[color]
            # box
            tagPadding = 30
            widthOffset = QtGui.QFontMetrics(fontMed10).width(tag) + tagPadding
            coords[2] = widthOffset
            tagColor = QtGui.QColor(*colorValues[0])
            smoothBox = QtGui.QPainterPath()
            smoothBox.addRoundedRect(QtCore.QRectF(*coords), 10, 10)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtGui.QPen(QtGui.QColor(*colorValues[1])))
            painter.fillPath(smoothBox, tagColor)

            # text
            coords[0] += tagPadding / 2  # pad the text in the box
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
            painter.setFont(fontMed10)
            painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, tag)
            # prepare for the next tag:
            coords[0] += widthOffset
            coords[0] -= tagPadding / 2  # remove text padding
            coords[0] += 5  # nice space between tags
            return coords

        # --------- top drop shadow -------
        coords = list(option.rect.getCoords())
        coords[3] = 5
        shadowRect = QtCore.QRect(*coords)
        grad = QtGui.QLinearGradient(
            shadowRect.topRight(),
            shadowRect.bottomRight()
        )
        grad.setColorAt(0, QtGui.QColor(255, 255, 255))
        grad.setColorAt(1, QtGui.QColor(235, 235, 235))
        painter.fillRect(shadowRect, grad)

        # --------- top row ----------
        ## item TN
        thumbnail = controller.getThumbnailFromProject(value)
        if thumbnail:
            topLeft = option.rect.topLeft()
            position = QtCore.QPoint(
                topLeft.x() + framePadding,
                topLeft.y() + framePadding + 12
            )
            painter.drawPixmap(position, thumbnail)

        ## item title
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setFont(fontMed20)
        title = value["PROJECT_NAME"]
        coords = list(option.rect.getCoords())
        coords[0] += framePadding + thumbnailDimensions + framePadding
        coords[1] += framePadding
        coords[2] += framePadding + thumbnailDimensions + framePadding
        coords[3] += framePadding
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, title)
        ## description
        painter.setFont(font10)
        descr = controller.getDescriptionFromProject(value)
        coords[1] += 34  # under title
        coords[3] += 34
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, descr)

        ## Status & Integrations
        coords[1] += 20  # under descr
        coords[3] += 20
        painter.setFont(fontBold10)
        painter.drawText(
            QtCore.QRect(*coords),
            QtCore.Qt.AlignLeft,
            "Status: "
        )
        widthOffset = QtGui.QFontMetrics(fontBold10).width("Status: ")
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(font10)
        statusStr = controller.getProjectStatusFromProject(value)
        painter.drawText(
            QtCore.QRect(*coords),
            QtCore.Qt.AlignLeft,
            statusStr
        )
        ### Only print integrations if there are any
        if controller.isProjectGitEnabled(value):
            kerning = 10
            widthOffset = QtGui.QFontMetrics(font10).width(statusStr)
            widthOffset += kerning
            coords[0] += widthOffset
            coords[2] += widthOffset
            painter.setFont(fontBold10)
            intr = "Integrations: "
            painter.drawText(
                QtCore.QRect(*coords),
                QtCore.Qt.AlignLeft,
                intr
            )
            widthOffset = QtGui.QFontMetrics(fontBold10).width(intr)
            coords[0] += widthOffset
            coords[2] += widthOffset
            gitIcon = QtGui.QPixmap("icons/git.png")
            gitIcon = gitIcon.scaledToHeight(20)
            position = QtCore.QPoint(coords[0], coords[1])
            painter.drawPixmap(position, gitIcon)

        ## tags
        coords = list(option.rect.getCoords())
        coords[0] += framePadding + thumbnailDimensions + framePadding
        coords[1] += framePadding + 34 + 20 + 27  # under status&int
        coords[2] += framePadding + thumbnailDimensions + framePadding
        coords[3] = 20 # tag height

        category = controller.getCategoryFromProject(value)
        if category:
            coords = paintTag(category, "blue", coords)

        ptype = controller.getProjectTypeFromProject(value)
        if ptype:
            coords = paintTag(ptype, "yellow", coords)

        for tag in controller.getTagsFromProject(value):
            if tag in [category, ptype]:
                # No sense in repeating info, just skip this
                continue
            coords = paintTag(tag, "grey", coords)

        # ----------------------------
        heightOffset = framePadding + 12 + thumbnailDimensions + 12 + 12
        coords = list(option.rect.getCoords())
        coords[1] += heightOffset
        coords[3] += heightOffset
        lineSeparator = QtGui.QPainterPath()
        lineSeparator.moveTo(coords[0] + 25, coords[1])
        lineSeparator.lineTo(coords[2] - 25, coords[1])
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200)))
        painter.drawPath(lineSeparator)
        # --------- middle row -------

        ## Created icon
        heightOffset = framePadding + 12 + thumbnailDimensions + 10 + 20
        coords = list(option.rect.getCoords())
        coords[0] += framePadding
        coords[1] += heightOffset
        coords[2] += framePadding
        coords[3] += heightOffset
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        userCreated = controller.getUserCreatedFromProject(value)
        painter.drawPixmap(upperLeft, userCreated)
        ## Created Label
        coords[0] += 30  # after icon
        coords[1] += 3   # centering at image
        coords[2] += 30
        coords[3] += 3
        painter.setFont(fontBold10)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        words = "Created: "
        widthOffset = QtGui.QFontMetrics(fontBold10).width(words)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, words)
        ## Created date
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(font10)
        created = controller.getDateCreatedFromProject(value)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, created)
        widthOffset = QtGui.QFontMetrics(font10).width(created)

        ## Modified icon
        coords[0] += widthOffset + 45  # lots of space between entries
        coords[1] -= 3  # remove text centering
        coords[2] += widthOffset + 45
        coords[3] -= 3
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        userModified = controller.getUserModifiedFromProject(value)
        painter.drawPixmap(upperLeft, userModified)
        ## Modified Label
        coords[0] += 30  # after icon
        coords[1] += 3   # centering at image
        coords[2] += 30
        coords[3] += 3
        painter.setFont(fontBold10)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        words = "Last Modified: "
        widthOffset = QtGui.QFontMetrics(fontBold10).width(words)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, words)
        ## Modified date
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(font10)
        modified = controller.getDateModifiedFromProject(value)
        widthOffset = QtGui.QFontMetrics(font10).width(modified)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, modified)

        ## Contributors Label
        coords[0] += widthOffset + 45  # lots of space between entries
        coords[2] += widthOffset + 45
        painter.setFont(fontBold10)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        words = "Contributors: "
        widthOffset = QtGui.QFontMetrics(fontBold10).width(words)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, words)
        ## Contributors Icons
        contributors = controller.getContributorsFromProject(value)
        coords[0] += widthOffset
        coords[1] -= 3  # remove text centering
        coords[2] += widthOffset
        coords[3] -= 3
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        for i, contributor in enumerate(contributors):
            if i > 0:
                coords[0] += 20  # move over from last icon
                # This isn't our first icon. We need to draw a white circle
                #  to separate the overlapping user icons before drawing
                #  the user icon.
                whiteCircle = QtGui.QPainterPath()
                coords[0] -= 3  # back up a touch
                coords[1] -= 2  # larger circle means nudge down
                whiteCircle.moveTo(coords[0], coords[1])
                whiteCircle.arcTo(coords[0], coords[1], 30, 30, 0, 360)
                whiteCircle.closeSubpath()
                whiteColor = QtGui.QColor(255, 255, 255)
                painter.fillPath(whiteCircle, whiteColor)
                coords[0] += 3  # undo offsets
                coords[1] += 2
            # TODO: If the number of contributors exceeds 5, draw instead of
            #  the fifth icon a grey circle with the +# indicating the number
            #  of contributors. Else draw the icon.
            iconSpot = QtCore.QPointF(coords[0], coords[1])
            painter.drawPixmap(iconSpot, contributor)

        # ----------------------------
        heightOffset = framePadding + 12 + thumbnailDimensions + 10 + 50
        coords = list(option.rect.getCoords())
        coords[1] += heightOffset
        coords[3] += heightOffset
        lineSeparator = QtGui.QPainterPath()
        lineSeparator.moveTo(coords[0] + 25, coords[1])
        lineSeparator.lineTo(coords[2] - 25, coords[1])
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200)))
        painter.drawPath(lineSeparator)
        # --------- bottom row -------

        ## Formats
        heightOffset = framePadding + 12 + thumbnailDimensions + 10 + 60
        coords = list(option.rect.getCoords())
        coords[0] += framePadding
        coords[1] += heightOffset
        coords[2] += framePadding
        coords[3] += heightOffset
        painter.setFont(fontBold10)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        words = "Formats: "
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, words)
        widthOffset = 90  # instead of metrics, the bottom row specifies
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(font10)
        ftypes = controller.getFileTypesFromProject(value)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, ftypes)

        ## Notes
        heightOffset = framePadding + 12 + thumbnailDimensions + 10 + 85
        coords = list(option.rect.getCoords())
        coords[0] += framePadding
        coords[1] += heightOffset
        coords[2] += framePadding
        coords[3] += heightOffset
        painter.setFont(fontBold10)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        words = "Notes: "
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, words)
        widthOffset = 90  # instead of metrics, the bottom row specifies
        coords[0] += widthOffset
        coords[2] += widthOffset
        painter.setFont(font10)
        notes = controller.getNotesPreviewFromProject(value)
        for note in notes:
            painter.drawText(
                QtCore.QRect(*coords),
                QtCore.Qt.AlignLeft,
                note
            )
            coords[1] += 18
            coords[3] += 18

        # --------- bottom drop shadow -------
        heightOffset = framePadding + 12 + thumbnailDimensions + 10 + 145
        coords = list(option.rect.getCoords())
        coords[1] += heightOffset
        coords[3] = 10
        shadowRect = QtCore.QRect(*coords)
        grad = QtGui.QLinearGradient(
            shadowRect.topRight(),
            shadowRect.bottomRight()
        )
        grad.setColorAt(0, QtGui.QColor(235, 235, 235))
        grad.setColorAt(1, QtGui.QColor(255, 255, 255))
        painter.fillRect(shadowRect, grad)




        painter.restore()

    def sizeHint(self, option, index):
        size = QtCore.QSize(200, 278)
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
