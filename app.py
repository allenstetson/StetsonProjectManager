
# std imports
import datetime
import os
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

#################
# Decorators
#################
def styledQt(cls):
    init = cls.__init__
    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)
        with open("./stylesheet.css") as fh:
            self.setStyleSheet(fh.read())
    cls.__init__ = __init__
    return cls


#################
# Classes
#################
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, labelText, color=None, parent=None):
        super(ClickableLabel, self).__init__(parent=parent)
        self.labelText = labelText
        self._build()

    def _build(self):
        self.setText(self.labelText)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            styleSheetText = ("text-decoration: underline;")
            self.setStyleSheet(styleSheetText)
        elif event.type() == QtCore.QEvent.Leave:
            styleSheetText = ("text-decoration: none;")
            self.setStyleSheet(styleSheetText)
        return False

    def mousePressEvent(self, event):
        super(ClickableLabel, self).mousePressEvent(event)
        self.clicked.emit()


class ComboBoxCompleter(QtWidgets.QComboBox):
    textEditFinished = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(ComboBoxCompleter, self).__init__(parent=parent)
        self.setEditable(True)
        self.completer = QtWidgets.QCompleter(self)
        self.completer.setCompletionMode(
            QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.completer.setPopup(self.view())
        self.completer.popup().setObjectName("ComboBoxCompleterList")
        self.filterProxyModel = QtCore.QSortFilterProxyModel(self)
        self.filterProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.model = QtGui.QStandardItemModel()

        self.setCompleter(self.completer)
        self.setModel(self.model)
        self.setFocusPolicy = QtCore.Qt.StrongFocus

        self.lineEdit().textEdited.connect(
            self.filterProxyModel.setFilterFixedString)
        self.lineEdit().returnPressed.connect(self._handleTextEditFinished)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)
        self.currentIndexChanged.connect(self._handleTextEditFinished)

    def _handleTextEditFinished(self):
        self.textEditFinished.emit()

    def addItems(self, items):
        for i, word in enumerate(items):
            item = QtGui.QStandardItem(word)
            self.model.setItem(i, 0, item)
        self.setModelColumn(0)

    def setModel(self, model):
        super(ComboBoxCompleter, self).setModel(model)
        self.filterProxyModel.setSourceModel(model)
        self.completer.setModel(self.filterProxyModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.filterProxyModel.setFilterKeyColumn(column)
        super(ComboBoxCompleter, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


class ImagePushButton(QtWidgets.QPushButton):
    def __init__(self, imagePath, dimensions=None, disabledPath=None,
                 fixedSize=True, parent=None, pressedPath=None,
                 rolloverPath=None, rotated=False):
        super(ImagePushButton, self).__init__(parent=parent)
        self._isRotated=rotated
        self.dimensions = dimensions or (None, None)
        self.pixmap = None
        self.pixmapDisabled = None
        self.pixmapNormal = None
        self.pixmapOver = None
        self.pixmapPressed = None
        self.stickyOn = False

        self._setPixmaps(imagePath, pressedPath, rolloverPath, disabledPath)
        self.pressed.connect(self.update)
        self.released.connect(self.update)
        if self._isRotated:
            self.rotateClockwise()
        if fixedSize:
            self.setFixedSize(self.sizeHint())

    def _setPixmaps(self, imagePath, pressedPath, rolloverPath, disabledPath):
        brokenImagePath = "./icons/photo_broken.png"
        if not os.path.exists(imagePath):
            imagePath = brokenImagePath
        self.pixmapNormal = QtGui.QPixmap(imagePath)
        if pressedPath:
            if not os.path.exists(pressedPath):
                pressedPath = brokenImagePath
            self.pixmapPressed = QtGui.QPixmap(pressedPath)
        else:
            self.pixmapPressed = self.pixmapNormal
        if rolloverPath:
            if not os.path.exists(rolloverPath):
                rolloverPath = brokenImagePath
            self.pixmapOver = QtGui.QPixmap(rolloverPath)
        else:
            #self.pixmapOver = self.pixmapNormal
            self.pixmapOver = QtGui.QPixmap(imagePath)
            painter = QtGui.QPainter(self.pixmapOver)
            painter.setCompositionMode(painter.CompositionMode_Overlay)
            painter.fillRect(self.pixmapOver.rect(), QtGui.QColor(155, 155, 155))
            painter.end()
        if disabledPath:
            if not os.path.exists(disabledPath):
                disabledPath = brokenImagePath
            self.pixmapDisabled = QtGui.QPixmap(disabledPath)
        else:
            self.pixmapDisabled = self.pixmapPressed
        self.pixmap = self.pixmapNormal

    def disable(self):
        self.pixmap = self.pixmapDisabled
        self.setEnabled(False)
        
    def enable(self):
        self.pixmap = self.pixmapNormal
        self.setEnabled(True)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def paintEvent(self, event):
        self.pixmap = self.pixmapNormal
        if self.underMouse():
            self.pixmap = self.pixmapOver
        if self.isDown():
            self.pixmap = self.pixmapPressed

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPixmap(event.rect(), self.pixmap)

    def rotateClockwise(self):
        transformation = QtGui.QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapDisabled = self.pixmapDisabled.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapNormal = self.pixmapNormal.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapOver = self.pixmapOver.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapPressed = self.pixmapPressed.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self._isRotated = True

    def rotateCounterClockwise(self):
        transformation = QtGui.QTransform().rotate(-90)
        self.pixmap = self.pixmap.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapDisabled = self.pixmapDisabled.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapNormal = self.pixmapNormal.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapOver = self.pixmapOver.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self.pixmapPressed = self.pixmapPressed.transformed(
            transformation,
            QtCore.Qt.SmoothTransformation
        )
        self._isRotated = False

    def sizeHint(self):
        if self.dimensions[0]:
            height = self.dimensions[0]
            width = self.dimensions[1] or \
                    self.pixmap.scaledToHeight(height).width()
        else:
            height = self.pixmap.height()
            width = self.pixmap.width()
        return QtCore.QSize(width, height)

    def toggleImageRotation(self):
        if self._isRotated:
            self.rotateCounterClockwise()
        else:
            self.rotateClockwise()

    def toggleSticky(self):
        if self.stickyOn:
            self.pixmap = self.pixmapNormal
            self.stickyOn = False
        else:
            self.pixmap = self.pixmapOver
            self.stickyOn = True
        self.update()


class TimeSpinBox(QtWidgets.QSpinBox):
    def textFromValue(self, num):
        return str(num).rjust(2, "0")


class TimePicker(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(TimePicker, self).__init__(parent=parent)
        startSpacer = QtWidgets.QSpacerItem(
            1,
            3,
            QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout = QtWidgets.QHBoxLayout()
        self.hourBox = TimeSpinBox(self)
        self.hourBox.setRange(1, 12)
        self.minBox = TimeSpinBox(self)
        self.minBox.setRange(0, 59)
        self.ampm = QtWidgets.QComboBox(self)
        self.ampm.addItems(["AM", "PM"])
        endSpacer = QtWidgets.QSpacerItem(
            1,
            3,
            QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout.addItem(startSpacer)
        self.layout.addWidget(self.hourBox)
        self.layout.addWidget(self.minBox)
        self.layout.addWidget(self.ampm)
        self.layout.addItem(endSpacer)
        self.setLayout(self.layout)

class DatePopup(QtWidgets.QDateTimeEdit):
    def __init__(self, before=True, *args, **kwargs):
        super(DatePopup, self).__init__(*args, **kwargs, calendarPopup=True)
        self.todayButton = QtWidgets.QPushButton(self.tr("Today"))
        self.todayButton.clicked.connect(self.updateToday)
        self.calendarWidget().layout().addWidget(self.todayButton)
        self.addTime()
        self.calendarWidget().setMinimumHeight(250)
        if before:
            self.setDateTime(QtCore.QDateTime.currentDateTime())
        else:
            past = datetime.datetime(2000, 1, 1)
            self.setDateTime(QtCore.QDateTime(past))
        self.dateChanged.connect(self._setTime)

    def _setTime(self):
        hour = self.timePicker.hourBox.value()
        minute = self.timePicker.minBox.value()
        ampm = self.timePicker.ampm.currentText()
        if ampm == "PM":
            hour = hour + 12
            if hour == 24:
                hour = 12
        time = QtCore.QTime(hour, minute)
        self.setTime(time)

    def addTime(self):
        self.timePicker = TimePicker(parent=self)
        self.calendarWidget().layout().addWidget(self.timePicker)

    def updateToday(self):
        self.todayButton.clearFocus()
        today = QtCore.QDate.currentDate()
        self.calendarWidget().setSelectedDate(today)


class FilterDateTime(QtWidgets.QFrame):
    def __init__(self, dateType=None, *args, **kwargs):
        super(FilterDateTime, self).__init__(*args, **kwargs)
        self.dateType = dateType or "modified"
        self.layout = QtWidgets.QVBoxLayout()
        self._buildLayout()
        self.setLayout(self.layout)
        self.species = "dateTime"

    def _buildLayout(self):
        if self.dateType == "modified":
            title = QtWidgets.QLabel("LAST MODIFIED")
        else:
            title = QtWidgets.QLabel("CREATED")
        title.setObjectName("filterTitle")
        self.layout.addWidget(title)

        beforeRow = QtWidgets.QHBoxLayout()
        before = QtWidgets.QLabel("before")
        #before.setObjectName("filterTitle")
        beforeRow.addWidget(before)

        self.datePopupBefore = DatePopup(before=True, parent=self)
        beforeRow.addWidget(self.datePopupBefore)
        self.layout.addLayout(beforeRow)

        afterRow = QtWidgets.QHBoxLayout()
        after = QtWidgets.QLabel("after")
        #after.setObjectName("filterTitle")
        afterRow.addWidget(after)

        self.datePopupAfter = DatePopup(before=False, parent=self)
        afterRow.addWidget(self.datePopupAfter)
        self.layout.addLayout(afterRow)

    def getFilterData(self):
        species = self.species + self.dateType.title()
        data = {
            "before": self.datePopupBefore.dateTime(),
            "after": self.datePopupAfter.dateTime()
        }
        return (species, data)


@styledQt
class FilterTagNewStyle(QtWidgets.QFrame):
    boxStateChanged = QtCore.pyqtSignal(object, int)
    def __init__(self, include=True, parent=None):
        super(FilterTagNewStyle, self).__init__(parent=parent)
        self.include = include
        self.layout = QtWidgets.QVBoxLayout()
        self._buildLayout()
        self.setLayout(self.layout)
        self.setMaximumHeight(200)
        self.species = "tag"

    def _buildLayout(self):
        # Include Tags line
        inclTagsLineLayout = QtWidgets.QHBoxLayout()
        inclTagsLineLayout.setContentsMargins(0, 0, 0, 0)
        if self.include:
            title = QtWidgets.QLabel("INCLUDE TAGS (")
        else:
            title = QtWidgets.QLabel("EXCLUDE TAGS (")
        title.setObjectName("filterTitle")
        inclTagsLineLayout.addWidget(title)
        self.btnClearFilter = ClickableLabel("Clear")
        self.btnClearFilter.clicked.connect(self.clearTags)
        inclTagsLineLayout.addWidget(self.btnClearFilter)
        endParen = QtWidgets.QLabel(")")
        endParen.setObjectName("filterTitle")
        inclTagsLineLayout.addWidget(endParen)
        spacer = QtWidgets.QSpacerItem(
            10,
            1,
            QtWidgets.QSizePolicy.Expanding)
        inclTagsLineLayout.addItem(spacer)
        self.layout.addLayout(inclTagsLineLayout)

        # Combo Box
        self.cbCompleterTag = ComboBoxCompleter(self)
        self.cbCompleterTag.textEditFinished.connect(self._toggleCheckBox)
        self.layout.addWidget(self.cbCompleterTag)
        self.cbCompleterTag.addItems(controller.getAllTags())

        # Scroll Area with List
        scrollAreaList = QtWidgets.QScrollArea()
        itemList = QtWidgets.QWidget()
        self.itemListLayout = QtWidgets.QVBoxLayout()
        itemList.setLayout(self.itemListLayout)
        for item in controller.getAllTags():
            chkbx = QtWidgets.QCheckBox(item.title(), self)
            chkbx.stateChanged.connect(self._handleStateChange)
            self.itemListLayout.addWidget(chkbx)
        self.layout.addWidget(scrollAreaList)
        scrollAreaList.setWidget(itemList)

    def _handleStateChange(self, state):
        sender = self.sender()
        self.boxStateChanged.emit(sender, state)

    def _toggleCheckBox(self):
        tagName = self.cbCompleterTag.currentText()
        index = self.itemListLayout.count()
        while index >= 0:
            item = self.itemListLayout.itemAt(index)
            if not item:
                index -= 1
                continue
            itemName = item.widget().text().lower()
            if itemName == tagName:
                if item.widget().isChecked():
                    item.widget().setChecked(False)
                else:
                    item.widget().setChecked(True)
                break
            index -= 1

    def clearTags(self):
        index = self.itemListLayout.count()
        while index >= 0:
            item = self.itemListLayout.itemAt(index)
            if not item:
                index -= 1
                continue
            item.widget().setChecked(False)
            index -= 1

    def getFilterData(self):
        checkedTags = []
        index = self.itemListLayout.count()
        while index >= 0:
            item = self.itemListLayout.itemAt(index)
            if not item:
                index -= 1
                continue
            if item.widget().isChecked():
                tagName = item.widget().text().lower()
                checkedTags.append(tagName)
            index -= 1

        species = self.species
        if self.include:
            keyword = "include"
        else:
            keyword = "exclude"
        data = {keyword: checkedTags}
        return (species, data)

    def reactToStateChange(self, sender, state):
        tagName = sender.text()

        index = self.itemListLayout.count()
        while index >= 0:
            item = self.itemListLayout.itemAt(index)
            if not item:
                index -= 1
                continue
            if item.widget().text() == tagName:
                item.widget().setEnabled(not state)
                break
            index -= 1


class FilterTag(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(FilterTag, self).__init__(parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        self._searchType = "with tag"
        self._tagName = "home"
        self._title = "Tag"
        self.phrase = "default label message"

        self._buildLayout()
        self.setLayout(self.layout)

    def _buildLayout(self):
        self.titleLabel = QtWidgets.QLabel(self._title)
        self.layout.addWidget(self.titleLabel)
        self.phraseLabel = QtWidgets.QLabel()
        self.setPhrase()
        self.layout.addWidget(self.phraseLabel)

    def setPhrase(self):
        self.phrase = "{}: \"{}\"".format(self._searchType, self._tagName)
        self.phraseLabel.setText(self.phrase)

    @property
    def searchType(self):
        return self._searchType

    @searchType.setter
    def searchType(self, searchType):
        self._searchType = searchType
        self.setPhrase()

    @property
    def tagName(self):
        return self._tagName

    @tagName.setter
    def tagName(self, newtag):
        self._tagName = newtag
        self.setPhrase()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.titleLabel.setText(self._title)


class FilterTagEditor(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(FilterTagEditor, self).__init__(parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        self._buildLayout()
        self.setLayout(self.layout)
        self.setMaximumHeight(120)
        self.setStyleSheet("background-color: #DDDDDD")

    def _buildLayout(self):
        titleLabel = QtWidgets.QLabel("Tag")
        titleLabel.setFont(QtGui.QFont("Roboto", 14, QtGui.QFont.Bold))
        self.layout.addWidget(titleLabel)

        self.optionsLayout = QtWidgets.QHBoxLayout()
        self.cbAction = QtWidgets.QComboBox()
        self.cbAction.addItems(["with tag", "without tag"])
        self.optionsLayout.addWidget(self.cbAction)

        self.cbTags = QtWidgets.QComboBox()
        self.cbTags.addItems(controller.getAllTags())
        self.optionsLayout.addWidget(self.cbTags)
        self.layout.addLayout(self.optionsLayout)

        #bottom row
        actionButtonsLayout = QtWidgets.QHBoxLayout()
        self.btnDuplicate = ImagePushButton("./icons/copy.png", dimensions=(20, None))
        actionButtonsLayout.addWidget(self.btnDuplicate)
        spacer = QtWidgets.QSpacerItem(
            20,
            1,
            QtWidgets.QSizePolicy.Expanding
            )
        actionButtonsLayout.addItem(spacer)
        self.btnMute = ImagePushButton("./icons/invisible.png", dimensions=(20, None))
        actionButtonsLayout.addWidget(self.btnMute)
        self.btnDelete = ImagePushButton("./icons/delete.png", dimensions=(20, None))
        actionButtonsLayout.addWidget(self.btnDelete)
        self.layout.addLayout(actionButtonsLayout)

    @property
    def action(self):
        return self.cbAction.currentText()

    @action.setter
    def action(self, newAction):
        self.cbAction.setCurrentText(newAction)

    @property
    def tagName(self):
        return self.cbTags.currentText()

    @tagName.setter
    def tagName(self, newTag):
        self.cbTags.setCurrentText(newTag)


@styledQt
class FilterUser(QtWidgets.QFrame):
    boxStateChanged = QtCore.pyqtSignal(object, int)
    def __init__(self, mode=None, parent=None):
        super(FilterUser, self).__init__(parent=parent)
        self.mode = mode or "creator"
        self.layout = QtWidgets.QVBoxLayout()
        self._buildLayout()
        self.setLayout(self.layout)
        self.setMaximumHeight(200)
        self.species = "user"

    def _buildLayout(self):
        # Title
        title = QtWidgets.QLabel("{}".format(self.mode.upper()))
        title.setObjectName("filterTitle")
        self.layout.addWidget(title)

        # Scroll Area with List
        scrollAreaList = QtWidgets.QScrollArea()
        itemList = QtWidgets.QWidget()
        self.itemListLayout = QtWidgets.QVBoxLayout()
        itemList.setLayout(self.itemListLayout)
        if self.mode == "creator":
            users = controller.getAllUsersCreated()
        else:
            users = controller.getAllUsersModified()
        for user in users:
            chkbx = QtWidgets.QCheckBox(user, self)
            chkbx.setIcon(controller.getIconForUser(user))
            chkbx.stateChanged.connect(self._handleStateChange)
            self.itemListLayout.addWidget(chkbx)
        self.layout.addWidget(scrollAreaList)
        scrollAreaList.setWidget(itemList)

    def _handleStateChange(self, state):
        sender = self.sender()
        self.boxStateChanged.emit(sender, state)

    def getFilterData(self):
        species = self.species + self.mode.title()
        return (species, self.getSelectedUsers())

    def getSelectedUsers(self):
        users = []
        index = self.itemListLayout.count()
        while index >= 0:
            item = self.itemListLayout.itemAt(index)
            if not item:
                index -= 1
                continue
            if item.widget().isChecked() and item.widget().isEnabled():
                users.append(item.widget().text())
            index -= 1
        return sorted(users)


class StetsonHPMMainWindow(QtWidgets.QMainWindow):
    """Main window for Stetson HPM, containing the main widget.

    Args:
        parent (QtWidgets.QWidget): The parent of this widget (optional).
    
    """
    def __init__(self, parent=None):
        super(StetsonHPMMainWindow, self).__init__(parent=parent)
        self.setWindowTitle("Stetson HPM")
        #app.setWindowIcon()
        self.setMinimumSize(QtCore.QSize(500, 350))
        self.resize(QtCore.QSize(1020, 768))
        self.setCentralWidget(StetsonHPMMainWidget(self))


@styledQt
class StetsonHPMMainWidget(QtWidgets.QFrame):
    """Main widget for Stetson HPM.

    This widget has a top bar and a body. Depending on the tool state, the body
    could hold the project browser with filter or the project inspector, etc.

    Args:
        parent (QtWidgets.QWidget): The parent of this widget (optional).
    
    """
    def __init__(self, parent=None):
        super(StetsonHPMMainWidget, self).__init__(parent=parent)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.buildLayout()
        self.setLayout(self.mainLayout)

    def buildLayout(self):
        windowStack = SHPMWindowStack(self)
        self.mainLayout.addWidget(windowStack)

@styledQt
class SearchBox(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(SearchBox, self).__init__(*args, **kwargs)
        self.setPlaceholderText("Search")
        self.setObjectName("SearchBox")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.clear()
        super(SearchBox, self).keyPressEvent(event)


class SHPMTopBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(SHPMTopBar, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        # search
        searchBox = SearchBox(parent=self)
        searchBox.setMinimumWidth(150)
        searchBox.setMaximumWidth(150)
        self.layout.addWidget(searchBox)
        #space
        spacer = QtWidgets.QSpacerItem(
            400,
            10,
            QtWidgets.QSizePolicy.Expanding
            )
        self.layout.addItem(spacer)
        # user
        self.profilePicture = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("samples/allen.png")
        self.profilePicture.setPixmap(
            pixmap.scaledToHeight(40)
            )
        self.profilePicture.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.profilePicture)
        # button
        self.btnNewProject = QtWidgets.QPushButton(self)
        self.btnNewProject.setText("New Project")
        self.layout.addWidget(self.btnNewProject)

        self.setLayout(self.layout)


class SHPMWindowStack(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(SHPMWindowStack, self).__init__(parent=parent)
        self.widget1 = SHPMProjectBrowser()
        self.widget2 = SHPMProjectInspector()
        self.addWidget(self.widget1)
        self.addWidget(self.widget2)


class SHPMProjectBrowser(QtWidgets.QFrame):
    projectBrowserFilterChanged = QtCore.pyqtSignal()
    def  __init__(self, parent=None):
        super(SHPMProjectBrowser, self).__init__(parent=parent)
        self.filters = []
        self.layout = QtWidgets.QHBoxLayout()

        # declare list -- must come before filter declaration
        self.projectList = SHPMProjectBrowserList(parent=self)
        self.projectList.filterUpdateFinished.connect(self.updateNumResults)
        # Project Filter
        self.projectFilter = SHPMProjectBrowserFilter(parent=self)

        # Project List
        rightFrame = QtWidgets.QFrame()
        rightFrameLayout = QtWidgets.QVBoxLayout()
        rightFrame.setLayout(rightFrameLayout)

        # Top Bar        
        self.topBar = SHPMTopBar()
        rightFrameLayout.addWidget(self.topBar)

        # HLine
        line = QHLine(self)
        rightFrameLayout.addWidget(line)

        sortLayout = QtWidgets.QHBoxLayout()
        ## Num Results
        lblShowing = QtWidgets.QLabel("showing ")
        lblShowing.setObjectName("textLight")
        self.lblNumResults = QtWidgets.QLabel("68 results")
        self.lblNumResults.setObjectName("textBold")
        sortLayout.addWidget(lblShowing)
        sortLayout.addWidget(self.lblNumResults)
        ## spacer
        spacer = QtWidgets.QSpacerItem(
            300,
            10,
            QtWidgets.QSizePolicy.Expanding)
        sortLayout.addItem(spacer)
        ## Sorter
        sortLabel = QtWidgets.QLabel("Sort by:")
        sortLabel.setObjectName("textLight")
        sortLayout.addWidget(sortLabel)
        self.sortBy = QtWidgets.QComboBox()
        self.sortBy.setMinimumWidth(80)
        sortOptions = ["Title ", "Created", "Modified", "Status"]
        for option in sortOptions:
            self.sortBy.addItem(option + " (descending)")
            self.sortBy.addItem(option + " (ascending)")

        self.sortBy.setEditable(True)
        self.sortBy.lineEdit().setReadOnly(True)
        self.sortBy.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        self.sortBy.setObjectName("comboSortBy")
        sortLayout.addWidget(self.sortBy)
        ## -
        rightFrameLayout.addLayout(sortLayout)
        ##List
        rightFrameLayout.addWidget(self.projectList)
        # Splitter
        self.browserSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.browserSplitter.addWidget(self.projectFilter)
        self.browserSplitter.addWidget(rightFrame)
        self.layout.addWidget(self.browserSplitter)
        # Connect filter to list
        self.projectFilter.dirtyFilter.connect(self.projectList.filterList)
        self.setLayout(self.layout)
        self.updateNumResults()

    def registerFilter(self, filterObject):
        self.projectList.registerFilter(filterObject)

    def updateNumResults(self):
        num = self.projectList.listModel.rowCount()
        self.lblNumResults.setText("{} results".format(num))


@styledQt
class SHPMProjectBrowserFilter(QtWidgets.QFrame):
    dirtyFilter = QtCore.pyqtSignal()
    def  __init__(self, parent=None, *args, **kwargs):
        super(SHPMProjectBrowserFilter, self).__init__(parent=parent, *args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self._buildLayout()
        self.setLayout(self.layout)
        self.setMaximumWidth(250)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)

    def _buildLayout(self):
        panelScrollArea = QtWidgets.QScrollArea()
        panelScrollWidget = QtWidgets.QWidget()
        panelScrollWidget.setMinimumHeight(1000)
        panelScrollLayout = QtWidgets.QVBoxLayout()

        self.filterTagInclude = FilterTagNewStyle()
        controller.registerProjectBrowserFilter(self.filterTagInclude)
        panelScrollLayout.addWidget(self.filterTagInclude)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        self.filterTagExclude = FilterTagNewStyle(include=False)
        controller.registerProjectBrowserFilter(self.filterTagExclude)
        panelScrollLayout.addWidget(self.filterTagExclude)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        # Connect mutually exclusive widgets
        self.filterTagInclude.boxStateChanged.connect(
                self.filterTagExclude.reactToStateChange)
        self.filterTagExclude.boxStateChanged.connect(
                self.filterTagInclude.reactToStateChange)

        self.filterDateTimeModified = FilterDateTime(dateType="modified")
        controller.registerProjectBrowserFilter(self.filterDateTimeModified)
        panelScrollLayout.addWidget(self.filterDateTimeModified)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        self.filterDateTimeCreated = FilterDateTime(dateType="created")
        controller.registerProjectBrowserFilter(self.filterDateTimeCreated)
        panelScrollLayout.addWidget(self.filterDateTimeCreated)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        self.filterUserCreated = FilterUser(mode="creator")
        controller.registerProjectBrowserFilter(self.filterUserCreated)
        panelScrollLayout.addWidget(self.filterUserCreated)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        self.filterUserContributor = FilterUser(mode="contributor")
        controller.registerProjectBrowserFilter(self.filterUserContributor)
        panelScrollLayout.addWidget(self.filterUserContributor)
        line = QHLine(self)
        panelScrollLayout.addWidget(line)

        panelScrollWidget.setLayout(panelScrollLayout)
        panelScrollArea.setWidget(panelScrollWidget)
        self.layout.addWidget(panelScrollArea)

        # Connect browser list to filters
        self.filterUserCreated.boxStateChanged.connect(self.emitDirtyFilter)
        self.filterUserContributor.boxStateChanged.connect(self.emitDirtyFilter)
        self.filterTagInclude.boxStateChanged.connect(self.emitDirtyFilter)
        self.filterTagExclude.boxStateChanged.connect(self.emitDirtyFilter)


    def emitDirtyFilter(self):
        self.dirtyFilter.emit()


class SHPMFilterListModel(QtCore.QAbstractListModel):
    def __init__(self, filterTypes, parent=None):
        super(SHPMFilterListModel, self).__init__(parent=parent)
        self.filterTypes = filterTypes

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.filterTypes[index.row()])
        else:
            return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.filterTypes)


class SHPMFilterDelegate(QtWidgets.QItemDelegate):
    def _handleCloseEditor(self, editor):
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)

    def createEditor(self, parent, option, index):
        filterType = index.data(QtCore.Qt.DisplayRole)
        if isinstance(filterType, FilterTag):
            filterEditor = FilterTagEditor(parent=parent)
            filterEditor.btnDuplicate.clicked.connect(
                lambda: self._handleCloseEditor(filterEditor)
            )
            return filterEditor

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        backgroundColorSelected = QtGui.QColor(230, 240, 248)

        # item background
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(backgroundColorSelected))
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawRect(option.rect)

        # item
        item = index.data(QtCore.Qt.DisplayRole)
        if not item:
            return
        fontMed10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Medium)
        fontBold14 = QtGui.QFont("Roboto", 14, QtGui.QFont.Bold)
        framePadding = 10

        coords = list(option.rect.getCoords())
        coords[0] += framePadding
        coords[1] += framePadding
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setFont(fontBold14)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, item.title)

        coords[1] += 30
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setFont(fontMed10)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, item.phrase)

        painter.restore()

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = index.data(QtCore.Qt.DisplayRole)
        editor.action = item.searchType
        editor.tagName = item.tagName
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        if isinstance(index.data(), FilterTag):
            newWord = "Allen"  # really, get this from the editor
            index.data().searchType = editor.action
            index.data().tagName = editor.tagName
            model.setData(index, index.data())
        else:
            super(SHPMFilterDelegate, self).setModelData(editor, model, index)

    def sizeHint(self, option, index):
        size = QtCore.QSize(100, 100)
        return size


class SHPMProjectBrowserDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        #FIXME: This gets continually called/calculated on mouse move.
        #  Somehow ensure that this happens once, caches, and serves the cache
        painter.save()
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        #backgroundColorSelected = QtGui.QColor(230, 240, 248)
        backgroundColorSelected = QtGui.QColor(15, 74, 122)

        # item background
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawRect(option.rect)
        # SELECTION BOX
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_Selected:
            # paint a border
            ## draw the selection rect
            coords = list(option.rect.getCoords())
            coords[1] += 5  # account for shadows
            height = coords[3] - coords[1]
            coords[3] -= 15
            coords[3] = height - 15
            smoothBox = QtGui.QPainterPath()
            smoothBox.addRoundedRect(QtCore.QRectF(*coords), 5, 5)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.fillPath(smoothBox, backgroundColorSelected)

            ## fill the interior with white
            coords[0] += 3  # border of 3
            coords[1] += 3
            coords[2] -= 6
            coords[3] -= 6
            smoothBox = QtGui.QPainterPath()
            smoothBox.addRoundedRect(QtCore.QRectF(*coords), 4, 4)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.fillPath(smoothBox, QtCore.Qt.white)

        # item
        project = index.data(QtCore.Qt.DisplayRole)
        if not project:
            return

        framePadding = 25
        thumbnailDimensions = 80

        # Common Fonts
        font10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Normal)
        fontMed10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Medium)
        fontMed20 = QtGui.QFont("Roboto", 20, QtGui.QFont.Medium)
        fontBold10 = QtGui.QFont("Roboto", 10, QtGui.QFont.Bold)
        fontBold25 = QtGui.QFont("Roboto", 25, QtGui.QFont.Bold)

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
        grad.setColorAt(0, QtGui.QColor(246, 248, 250))
        grad.setColorAt(1, QtGui.QColor(243, 247, 251))
        painter.fillRect(shadowRect, grad)

        # --------- top row ----------
        ## item TN
        thumbnail = controller.getThumbnailFromProject(project)
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
        title = controller.getTitleFromProject(project)
        coords = list(option.rect.getCoords())
        coords[0] += framePadding + thumbnailDimensions + framePadding
        coords[1] += framePadding
        coords[2] += framePadding + thumbnailDimensions + framePadding
        coords[3] += framePadding
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, title)
        ## description
        painter.setFont(font10)
        descr = controller.getDescriptionFromProject(project)
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
        statusStr = controller.getProjectStatusFromProject(project)
        painter.drawText(
            QtCore.QRect(*coords),
            QtCore.Qt.AlignLeft,
            statusStr
        )
        ### Only print integrations if there are any
        if controller.getIntegrationsFromProject(project):
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
            for integ in controller.getIntegrationsFromProject(project):
                position = QtCore.QPoint(coords[0], coords[1])
                painter.drawPixmap(position, integ)
                coords[0] += 22

        ## tags
        coords = list(option.rect.getCoords())
        coords[0] += framePadding + thumbnailDimensions + framePadding
        coords[1] += framePadding + 34 + 20 + 27  # under status&int
        coords[2] += framePadding + thumbnailDimensions + framePadding
        coords[3] = 20 # tag height

        category = controller.getCategoryFromProject(project)
        if category:
            coords = paintTag(category, "blue", coords)

        ptype = controller.getProjectTypeFromProject(project)
        if ptype:
            coords = paintTag(ptype, "yellow", coords)

        for tag in controller.getTagsFromProject(project):
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
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100)))
        else:
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
        userCreated = controller.getUserCreatedFromProject(project)
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
        created = controller.getDateCreatedFromProject(project)
        painter.drawText(QtCore.QRect(*coords), QtCore.Qt.AlignLeft, created)
        widthOffset = QtGui.QFontMetrics(font10).width(created)

        ## Modified icon
        coords[0] += widthOffset + 45  # lots of space between entries
        coords[1] -= 3  # remove text centering
        coords[2] += widthOffset + 45
        coords[3] -= 3
        upperLeft = QtCore.QPointF(coords[0], coords[1])
        userModified = controller.getUserModifiedFromProject(project)
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
        modified = controller.getDateModifiedFromProject(project)
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
        contributors = controller.getContributorsFromProject(project)
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
                if option.state & QtWidgets.QStyle.State_Selected:
                    # if the background color ever changes during selection,
                    #  uncomment this line and delete the following:
                    #painter.fillPath(whiteCircle, backgroundColorSelected)
                    painter.fillPath(whiteCircle, whiteColor)
                else:
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
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100)))
        else:
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
        ftypes = controller.getFileTypesFromProject(project)
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
        notes = controller.getNotesPreviewFromProject(project)
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
        grad.setColorAt(0, QtGui.QColor(243, 247, 251))
        grad.setColorAt(1, QtGui.QColor(246, 248, 250))
        painter.fillRect(shadowRect, grad)

        painter.restore()

    def sizeHint(self, option, index):
        size = QtCore.QSize(200, 278)
        return size


class SHPMProjectBrowserList(QtWidgets.QFrame):
    filterUpdateFinished = QtCore.pyqtSignal()
    def  __init__(self, parent=None):
        super(SHPMProjectBrowserList, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        allProjects = controller.getAllProjects()
        self.listModel = SHPMProjectBrowserListProxyModel(allProjects, self)
        self.listModel.filterUpdateFinished.connect(self._handleFilterFinished)
        self.listDelegate = SHPMProjectBrowserDelegate(self)
        self.listView = QtWidgets.QListView()
        self.listView.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listView.setModel(self.listModel)
        self.listView.setItemDelegate(self.listDelegate)
        self.layout.addWidget(self.listView)

        self.setLayout(self.layout)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)

    def _handleFilterFinished(self):
        self.filterUpdateFinished.emit()

    def filterList(self):
        self.listModel.handleFilterChange()

    def registerFilter(self, filterObject):
        self.listModel.registerFilter(filterObject)


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


class SHPMProjectBrowserListProxyModel(QtCore.QSortFilterProxyModel):
    filterUpdateFinished = QtCore.pyqtSignal()
    def  __init__(self, listData, parent=None):
        super(SHPMProjectBrowserListProxyModel, self).__init__(parent=parent)
        self._registeredFilters = []
        self.setSourceModel(SHPMProjectBrowserListModel(listData))

    def filterAcceptsRow(self, sourceRow, sourceParent):
        idx = self.sourceModel().index(sourceRow, 0, sourceParent).row()
        itemData = self.sourceModel().listData[idx]
        for filterObject in self._registeredFilters:
            species, filterData = filterObject.getFilterData()
            # TAGS
            if species == "tag":
                pTags = controller.getTagsFromProject(itemData, extraTags=True)
                iTags = filterData.get("include", [])
                eTags = filterData.get("exclude", [])
                if iTags and not any([x for x in iTags if x in pTags]):
                    return False
                if eTags and any([x for x in eTags if x in pTags]):
                    return False
            # CREATOR
            if species == "userCreator":
                pCreator = controller.getUserCreatedFromProject(
                    itemData,
                    icon=False)
                if filterData and not pCreator in filterData:
                    return False
            # CONTRIBUTORS
            if species == "userContributor":
                pContributors = controller.getContributorsFromProject(
                    itemData,
                    icons=False)
                if filterData and not any(
                        [x for x in filterData if x in pContributors]):
                    return False
        return True

    def handleFilterChange(self):
        # This calls filterAcceptsRow:
        self.invalidateFilter()
        self.filterUpdateFinished.emit()

    def registerFilter(self, filterObject):
        if not hasattr(filterObject, "getFilterData"):
            msg = "Filter object {} lacks required method 'getFilterData'"
            msg = msg.filter(filterObject)
            raise ValueError(msg)
        self._registeredFilters.append(filterObject)


class SHPMProjectInspector(QtWidgets.QFrame):
    def  __init__(self, parent=None):
        super(SHPMProjectInspector, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        mylabel = QtWidgets.QLabel("Inspector")
        self.layout.addWidget(mylabel)
        self.setLayout(self.layout)

class QHLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(QHLine, self).__init__(parent=parent)
        #self.setFrameShape(QtWidgets.QFrame.HLine)
        #self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setMinimumHeight(1)
        self.setMaximumHeight(1)
        self.setStyleSheet("background: #d1dceb;")
        self.setObjectName("QHLine")


def main():
    app = QtWidgets.QApplication(sys.argv)
    #Splash screen goes here

    mainWindow = StetsonHPMMainWindow()
    mainWindow.show()

    app.exec_()

if __name__ == "__main__":
    main()
