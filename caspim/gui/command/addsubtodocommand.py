
from PyQt5.QtWidgets import QUndoCommand


class AddSubToDoCommand( QUndoCommand ):

    def __init__(self, dataObject, parentToDo, newToDo, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.parentToDo = parentToDo
        self.newToDo = newToDo

        self.setText( "Nueva subtarea: " + newToDo.title )

    def redo(self):
        self.parentToDo.addSubItem( self.newToDo )
        self.data.todosChanged.emit()

    def undo(self):
        self.parentToDo.removeSubItem( self.newToDo )
        self.data.todosChanged.emit()
