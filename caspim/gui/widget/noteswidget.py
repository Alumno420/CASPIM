from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QMenu, QInputDialog
from PyQt5.QtWidgets import QLineEdit

from .. import uiloader


UiTargetClass, QtBaseClass = uiloader.load_ui_from_class_name( __file__ )


NOTES_BG_COLOR = "#35322f"


class SinglePageWidget( QWidget ):

    contentChanged = pyqtSignal()
    createToDo     = pyqtSignal( str )

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)

        self.content = ""
        self.changeCounter = 0

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( vlayout )
        self.textEdit = QTextEdit(self)
        self.textEdit.setContextMenuPolicy( Qt.CustomContextMenu )

#         self.textEdit.setStyleSheet( "background-color: #f7ec9d;" )
        self.setStyleSheet(
            """
            QTextEdit {
                background: %s;
            }
            """ % NOTES_BG_COLOR
        )

        vlayout.addWidget( self.textEdit )

        self.textEdit.textChanged.connect( self.textChanged )
        self.textEdit.customContextMenuRequested.connect( self.textEditContextMenuRequest )

    def getText(self):
        return self.textEdit.toPlainText()

    def textChanged(self):
        contentText = self.getText()
        newLength  = len( contentText )
        currLength = len( self.content )
        diff = abs( newLength - currLength )
        self.changeCounter += diff
        self.content = contentText
        if self.changeCounter > 24:
            self.changeCounter = 0
            self.contentChanged.emit()

    def textEditContextMenuRequest(self, point):
        menu = self.textEdit.createStandardContextMenu()
        convertAction = menu.addAction("Convert to ToDo")
        convertAction.triggered.connect( self._convertToToDo )
        selectedText = self.textEdit.textCursor().selectedText()
        if not selectedText:
            convertAction.setEnabled( False )
        globalPos = self.mapToGlobal( point )
        menu.exec_( globalPos )

    def _convertToToDo(self):
        selectedText = self.textEdit.textCursor().selectedText()
        if not selectedText:
            return
        self.createToDo.emit( selectedText )


class NotesWidget( QtBaseClass ):           # type: ignore

    addNote    = pyqtSignal( str )
    renameNote = pyqtSignal( str, str )
    removeNote = pyqtSignal( str )

    notesChanged = pyqtSignal()
    createToDo   = pyqtSignal( str )

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)
        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        self.ui.notes_tabs.setStyleSheet(
            """
            QTabWidget {
                background: %s;
            }
            QTabBar {
                background: %s;
            }
            """ % (NOTES_BG_COLOR, NOTES_BG_COLOR)
        )

        self.ui.notes_tabs.clear()
        self.addTab( "Ideas" )

    def getNotes(self):
        notes = dict()
        notesSize = self.ui.notes_tabs.count()
        for tabIndex in range(0, notesSize):
            title = self.ui.notes_tabs.tabText( tabIndex )
            pageWidget = self.ui.notes_tabs.widget( tabIndex )
            text = pageWidget.getText()
            notes[ title ] = text
        return notes

    def setNotes(self, notesDict):
        self.ui.notes_tabs.clear()
        for key, value in notesDict.items():
            self.addTab( key, value )

    def addTab(self, title, text=""):
        pageWidget = SinglePageWidget(self)
        pageWidget.textEdit.setText( text )
        pageWidget.contentChanged.connect( self.notesChanged )
        pageWidget.createToDo.connect( self.createToDo )
        self.ui.notes_tabs.addTab( pageWidget, title )

    def contextMenuEvent( self, event ):
        evPos     = event.pos()
        globalPos = self.mapToGlobal( evPos )
        tabBar    = self.ui.notes_tabs.tabBar()
        tabPos    = tabBar.mapFromGlobal( globalPos )
        tabIndex  = tabBar.tabAt( tabPos )

        contextMenu   = QMenu(self)
        newAction     = contextMenu.addAction("Nuevo")
        renameAction  = contextMenu.addAction("Renombrar")
        deleteAction  = contextMenu.addAction("Eliminar")

        if tabIndex < 0:
            renameAction.setEnabled( False )
            deleteAction.setEnabled( False )

        action = contextMenu.exec_( globalPos )

        if action == newAction:
            self._newTabRequest()
        elif action == renameAction:
            self._renameTabRequest( tabIndex )
        elif action == deleteAction:
            noteTitle = self.ui.notes_tabs.tabText( tabIndex )
            self.removeNote.emit( noteTitle )

    def _newTabRequest( self ):
        newTitle = self._requestTabName( "Anotaciones" )
        if len(newTitle) < 1:
            return
        self.addNote.emit( newTitle )

    def _renameTabRequest( self, tabIndex ):
        if tabIndex < 0:
            return
        oldTitle = self.ui.notes_tabs.tabText( tabIndex )
        newTitle = self._requestTabName(oldTitle)
        if not newTitle:
            # empty
            return
        self.renameNote.emit( oldTitle, newTitle )

    def _requestTabName( self, currName ):
        newText, ok = QInputDialog.getText( self,
                                            "Rename Note",
                                            "Note name:",
                                            QLineEdit.Normal,
                                            currName )
        if ok and newText:
            # not empty
            return newText
        return ""
