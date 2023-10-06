from PyQt5.QtWidgets import QUndoCommand

class EditTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, oldTask, newTask, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.oldTask = oldTask
        self.newTask = newTask

        self.setText( "Editar Proyecto: " + newTask.title )

    def redo(self):
        self.domainModel.replaceTask( self.oldTask, self.newTask )
        self.data.tasksChanged.emit()

    def undo(self):
        self.domainModel.replaceTask( self.newTask, self.oldTask )
        self.data.tasksChanged.emit()
