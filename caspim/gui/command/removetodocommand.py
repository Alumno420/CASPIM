from PyQt5.QtWidgets import QUndoCommand



class RemoveToDoCommand( QUndoCommand ):

    def __init__(self, dataObject, todo, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.todo = todo
        self.todoCoords = self.domainModel.getToDoCoords( todo )

        self.setText( "Eliminar experiencia: " + todo.title )

    def redo(self):
        removed = self.domainModel.removeToDo( self.todo )
        self.data.todosChanged.emit()

    def undo(self):
        self.domainModel.insertToDo( self.todo, self.todoCoords )
        self.data.todosChanged.emit()
