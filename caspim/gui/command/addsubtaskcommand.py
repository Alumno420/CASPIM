
from PyQt5.QtWidgets import QUndoCommand

class AddSubTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, parentTask, newTask, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.parentTask = parentTask
        self.newTask = newTask

        self.setText( "Nueva experiencia: " + newTask.title )

    def redo(self):
        self.parentTask.addSubItem( self.newTask )
        self.data.tasksChanged.emit()

    def undo(self):
        self.parentTask.removeSubItem( self.newTask )
        self.data.tasksChanged.emit()
