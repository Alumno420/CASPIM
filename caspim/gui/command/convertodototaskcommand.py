
from PyQt5.QtWidgets import QUndoCommand

from caspim.gui.command.addtaskcommand import AddTaskCommand
from caspim.gui.command.removetodocommand import RemoveToDoCommand

class ConvertToDoToTaskCommand( QUndoCommand ):

    def __init__(self, dataObject, currentTodo, newTask, parentCommand=None):
        super().__init__(parentCommand)

        AddTaskCommand( dataObject, newTask, self )
        RemoveToDoCommand( dataObject, currentTodo, self )

        self.setText( "Convertir experiencias a proyecto" )

#     def redo(self):
#         super().redo()

#     def undo(self):
#         super().undo()
