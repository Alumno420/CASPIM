from PyQt5.QtCore import QObject, QDate
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QCursor

from caspim.domainmodel.task import Task
from caspim.gui.dataobject import DataObject


class TaskContextMenu( QObject ):

    addNewTask      = pyqtSignal( QDate )
    addNewSubTask   = pyqtSignal( Task )
    editTask        = pyqtSignal( Task )
    removeTask      = pyqtSignal( Task )
    markCompleted   = pyqtSignal( Task )

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)

        self.contextMenu = QMenu(parentWidget)
        self.addTaskAction       = self.contextMenu.addAction("Nuevo Proyecto")
        self.addSubTaskAction    = self.contextMenu.addAction("Nueva Sub Tarea")
        self.editTaskAction      = self.contextMenu.addAction("Editar Proyecto")
        self.removeTaskAction    = self.contextMenu.addAction("Eliminar Proyecto")
        self.markCompletedAction = self.contextMenu.addAction("Marcar acabado")

    def connectData(self, dataObject: DataObject):
        self.addNewTask.connect( dataObject.addNewTask )
        self.addNewSubTask.connect( dataObject.addNewSubTask )
        self.editTask.connect( dataObject.editTask )
        self.removeTask.connect( dataObject.removeTask )
        self.markCompleted.connect( dataObject.markTaskCompleted )

    def show(self, task: Task = None, newTaskDate: QDate = None ):
        if task is None:
            self.showNewTask( newTaskDate )
            return

        self.addSubTaskAction.setEnabled( True )
        self.editTaskAction.setEnabled( True )
        self.removeTaskAction.setEnabled( True )
        if task.isCompleted():
            self.markCompletedAction.setEnabled( False )
        else:
            self.markCompletedAction.setEnabled( True )

        globalPos = QCursor.pos()
        action = self.contextMenu.exec_( globalPos )

        if action == self.addTaskAction:
            if newTaskDate is None:
                newTaskDate = QDate.currentDate()
            self.addNewTask.emit( newTaskDate )
        elif action == self.addSubTaskAction:
            self.addNewSubTask.emit( task )
        elif action == self.editTaskAction:
            self.editTask.emit( task )
        elif action == self.removeTaskAction:
            self.removeTask.emit( task )
        elif action == self.markCompletedAction:
            self.markCompleted.emit( task )

    def showNewTask(self, newTaskDate: QDate = None ):
        ## context menu on background
        self.addSubTaskAction.setEnabled( False )
        self.editTaskAction.setEnabled( False )
        self.removeTaskAction.setEnabled( False )
        self.markCompletedAction.setEnabled( False )

        globalPos = QCursor.pos()
        action = self.contextMenu.exec_( globalPos )

        if action == self.addTaskAction:
            if newTaskDate is None:
                newTaskDate = QDate.currentDate()
            self.addNewTask.emit( newTaskDate )