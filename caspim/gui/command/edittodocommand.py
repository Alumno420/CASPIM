from PyQt5.QtWidgets import QUndoCommand


class EditToDoCommand( QUndoCommand ):

    def __init__(self, dataObject, oldToDo, newToDo, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.oldToDo = oldToDo
        self.newToDo = newToDo

        self.setText( "Editar Experiencia: " + newToDo.title )

    def redo(self):
        self.domainModel.replaceToDo( self.oldToDo, self.newToDo )
        self.data.todosChanged.emit()

    def undo(self):
        self.domainModel.replaceToDo( self.newToDo, self.oldToDo )
        self.data.todosChanged.emit()
