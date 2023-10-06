
from PyQt5.QtWidgets import QUndoCommand


class AddTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, newTask, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.newTask = newTask

        self.setText( "Nuevo proyecto: " + newTask.title )

    def redo(self):
        self.domainModel.addTask( self.newTask )
        self.data.tasksChanged.emit()

    def undo(self):
        self.domainModel.removeTask( self.newTask )
        self.data.tasksChanged.emit()
