from PyQt5.QtWidgets import QUndoCommand

class MoveTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, taskCoords, parentTask, targetIndex, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.taskCoords = taskCoords
        self.task = self.domainModel.getTaskByCoords( taskCoords )
        self.parentTask  = parentTask
        self.targetIndex = targetIndex

        self.setText( "Mover proyecto: " + self.task.title )

    def redo(self):
        self.domainModel.removeTask( self.task )
        self.parentTask.addSubItem( self.task, self.targetIndex )
        self.data.tasksChanged.emit()

    def undo(self):
        self.parentTask.removeSubItem( self.task )
        self.domainModel.insertTask( self.task, self.taskCoords )
        self.data.tasksChanged.emit()
