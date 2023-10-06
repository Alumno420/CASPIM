from datetime import datetime

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QDesktopServices

from caspim.domainmodel.task import Task

from .. import uiloader


UiTargetClass, QtBaseClass = uiloader.load_ui_from_class_name( __file__ )


class TaskDetails( QtBaseClass ):           # type: ignore

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        #self.ui.recurrentWidget.setReadOnly( True )

        self.ui.descriptionEdit.anchorClicked.connect( self._openLink )
        

        self.setTask( None )

    def setTask(self, task: Task):
        if task is None:
            self.ui.titleEdit.clear()
            self.ui.descriptionEdit.clear()
            self.ui.completionLabel.clear()
            self.ui.priorityBox.setValue( 0 )
            todayDate = datetime.today()
            self.ui.startDateTime.setDateTime( todayDate )
            self.ui.dueDateTime.setDateTime( todayDate )
            #self.ui.reminderList.clear()
            #self.ui.recurrentWidget.setEnabled( False )
            return

        self.ui.titleEdit.setText( task.title )
        self.ui.descriptionEdit.setText( task.description )
        self.ui.completionLabel.setText( str(task.completed) + "%" )
        self.ui.priorityBox.setValue( task.priority )
        if task.occurrenceStart is None:
            self.ui.deadlineBox.setChecked( True )
            if task.occurrenceDue is not None:
                self.ui.startDateTime.setDateTime( task.occurrenceDue )
        else:
            self.ui.deadlineBox.setChecked( False )
            self.ui.startDateTime.setDateTime( task.occurrenceStart )
        if task.occurrenceDue is not None:
            self.ui.dueDateTime.setEnabled( True )
            self.ui.dueDateTime.setDateTime( task.occurrenceDue )
        else:
            self.ui.dueDateTime.setEnabled( False )
        #self.ui.reminderList.clear()

        #self.ui.reminderList.clear()
        '''
        remLen = 0
        if task.reminderList is not None:
            remLen = len(task.reminderList)
        for i in range( 0, remLen ):
            rem = task.reminderList[ i ]
            item = QListWidgetItem( rem.printPretty() )
            self.ui.reminderList.insertItem( i, item )

        self.ui.recurrentWidget.setTask( task )
        if task.recurrence is None:
            self.ui.recurrentWidget.setEnabled( False )
        else:
            self.ui.recurrentWidget.setEnabled( True )
        '''
    # pylint: disable=R0201
    def _openLink( self, link ):
        QDesktopServices.openUrl( link )
