import copy

from PyQt5.QtWidgets import QUndoCommand


class MarkToDoCompletedCommand( QUndoCommand ):

    def __init__(self, dataObject, todo, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.oldState = copy.deepcopy( todo )
        self.todo = todo
        self.todo.setCompleted()
        self.domainModel.replaceTask( self.todo, self.oldState )

        self.setText( "Marcar experiencia completada: " + todo.title )

    def redo(self):
        self.domainModel.replaceToDo( self.oldState, self.todo )
        self.data.todosChanged.emit()

    def undo(self):
        self.domainModel.replaceToDo( self.todo, self.oldState )
        self.data.todosChanged.emit()
