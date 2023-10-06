from PyQt5.QtWidgets import QUndoCommand

class RemoveTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, task, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.task = task
        self.taskCoords = self.domainModel.getTaskCoords( task )

        self.setText( "Eliminar proyecto: " + task.title )

    def redo(self):
        removed = self.domainModel.removeTask( self.task )
        self.data.tasksChanged.emit()

    def undo(self):
        self.domainModel.insertTask( self.task, self.taskCoords )
        self.data.tasksChanged.emit()
