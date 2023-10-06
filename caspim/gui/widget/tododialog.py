import copy

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from caspim.domainmodel.todo import ToDo

from .. import uiloader


UiTargetClass, QtBaseClass = uiloader.load_ui_from_class_name( __file__ )

class ToDoDialog( QtBaseClass ):           # type: ignore

    def __init__(self, todoObject, parentWidget=None):
        super().__init__(parentWidget)
        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        if todoObject is not None:
            self.todo = copy.deepcopy( todoObject )
        else:
            self.todo = ToDo()

        self.completed = self.todo.completed

        self.ui.titleEdit.setText( self.todo.title )
        self.ui.descriptionEdit.setText( self.todo.description )
        self.ui.completionSlider.setValue( self.todo.completed )
        self.ui.priorityBox.setValue( self.todo.priority )

        self.ui.titleEdit.textChanged.connect( self._titleChanged )
        self.ui.descriptionEdit.textChanged.connect( self._descriptionChanged )
        self.ui.descriptionEdit.anchorClicked.connect( self._openLink )
        self.ui.completionSlider.valueChanged.connect( self._completedChanged )
        self.ui.priorityBox.valueChanged.connect( self._priorityChanged )

        #self.ui.openLocalFilePB.clicked.connect( self._openLocalFile )
        #self.ui.openLocalDirPB.clicked.connect( self._openLocalDir )
        #self.ui.addUrlPB.clicked.connect( self._addUrl )

        self.finished.connect( self._finished )

    def _titleChanged(self, newValue):
        self.todo.title = newValue

    def _descriptionChanged(self):
        newValue = self.ui.descriptionEdit.toHtml()
        self.todo.description = newValue

    def _completedChanged(self, newValue):
        #self.todo.completed = newValue
        self.completed = newValue

    def _priorityChanged(self, newValue):
        self.todo.priority = newValue

    def _openLocalFile(self):
        fielDialog = QFileDialog( self )
        fielDialog.setFileMode( QFileDialog.ExistingFile )
        dialogCode = fielDialog.exec_()
        if dialogCode == QDialog.Rejected:
            return
        selectedFile = fielDialog.selectedFiles()[0]
        fileUrl = QUrl.fromLocalFile( selectedFile )
        self.ui.urlEdit.setText( fileUrl.toString() )

    def _openLocalDir(self):
        fielDialog = QFileDialog( self )
        fielDialog.setFileMode( QFileDialog.Directory )
        dialogCode = fielDialog.exec_()
        if dialogCode == QDialog.Rejected:
            return
        selectedFile = fielDialog.selectedFiles()[0]
        fileUrl = QUrl.fromLocalFile( selectedFile )
        self.ui.urlEdit.setText( fileUrl.toString() )

    def _addUrl(self):
        urlText = self.ui.urlEdit.text()
        if len(urlText) < 1:
            return
        hrefText = "<a href=\"%s\">%s</a> " % (urlText, urlText)
        self.ui.descriptionEdit.insertHtml( hrefText )
        self.ui.urlEdit.setText( "" )

    def _openLink( self, link ):
        self.ui.urlEdit.setText( link.toLocalFile() )
        QDesktopServices.openUrl( link )

    def _finished(self, _):
        self.todo.completed = self.completed
