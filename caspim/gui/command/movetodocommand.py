from PyQt5.QtWidgets import QUndoCommand

class MoveToDoCommand( QUndoCommand ):

    def __init__(self, dataObject, todoCoords, parentToDo, targetIndex, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.todoCoords = todoCoords
        self.todo = self.domainModel.getToDoByCoords( todoCoords )
        self.parentToDo  = parentToDo
        self.targetIndex = targetIndex

        self.setText( "Mover experiencia: " + self.todo.title )

    def redo(self):
        self.domainModel.removeToDo( self.todo )
        self.parentToDo.addSubItem( self.todo, self.targetIndex )
        self.data.todosChanged.emit()

    def undo(self):
        self.parentToDo.removeSubItem( self.todo )
        self.domainModel.insertToDo( self.todo, self.todoCoords )
        self.data.todosChanged.emit()
