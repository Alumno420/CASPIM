import copy

from PyQt5.QtWidgets import QUndoCommand


class MarkTaskCompletedCommand( QUndoCommand ):

    def __init__(self, dataObject, task, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.oldState = copy.deepcopy( task )
        self.task = task
        self.task.setCompleted()
        self.domainModel.replaceTask( self.task, self.oldState )

        self.setText( "Marcar proyecto completado: " + task.title )

    def redo(self):
        self.domainModel.replaceTask( self.oldState, self.task )
        self.data.tasksChanged.emit()

    def undo(self):
        self.domainModel.replaceTask( self.task, self.oldState )
        self.data.tasksChanged.emit()
