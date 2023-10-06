from PyQt5.QtGui import QDesktopServices

from caspim.domainmodel.todo import ToDo

from .. import uiloader


UiTargetClass, QtBaseClass = uiloader.load_ui_from_class_name( __file__ )


class ToDoDetails( QtBaseClass ):           # type: ignore

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)
        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        self.ui.descriptionEdit.anchorClicked.connect( self._openLink )

        self.setToDo( None )

    def setToDo(self, todo: ToDo):
        if todo is None:
            self.ui.titleEdit.clear()
            self.ui.descriptionEdit.clear()
            self.ui.completionLabel.clear()
            self.ui.priorityBox.setValue( 0 )
            return

        self.ui.titleEdit.setText( todo.title )
        self.ui.descriptionEdit.setText( todo.description )
        self.ui.completionLabel.setText( str(todo.completed) + "%" )
        self.ui.priorityBox.setValue( todo.priority )

    # pylint: disable=R0201
    def _openLink( self, link ):
        QDesktopServices.openUrl( link )
