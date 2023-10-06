

from PyQt5.QtWidgets import QUndoCommand


class AddToDoCommand( QUndoCommand ):

    def __init__(self, dataObject, newToDo, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.newToDo = newToDo

        self.setText( "Nueva experiencia: " + newToDo.title )

    def redo(self):
        self.domainModel.addToDo( self.newToDo )
        self.data.todosChanged.emit()

    def undo(self):
        self.domainModel.removeToDo( self.newToDo )
        self.data.todosChanged.emit()
