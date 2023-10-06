import abc
import datetime

from PyQt5.QtWidgets import QCalendarWidget

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu


class NavCalendarHighlightModel():

    @abc.abstractmethod
    def isHighlighted(self, date: QDate ):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def isOccupied(self, date: QDate ):
        raise NotImplementedError('You need to define this method in derived class!')


class NavCalendar( QCalendarWidget ):

    addTask  = pyqtSignal( QDate )

    def __init__( self, *args ):
        QCalendarWidget.__init__( self, *args )

        self.cellsTable = self.findChild( QTableView )

        self.taskColor = QColor( self.palette().color( QPalette.Highlight) )
        self.taskColor.setAlpha( 64 )
        self.occupiedColor = QColor( QColor(10, 10, 160) )
        self.occupiedColor.setAlpha( 64 )

        self.highlightModel = None
        self.selectionChanged.connect( self.updateCells )

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)

        if self.isHighlighted( date ) is True:
            painter.fillRect( rect, self.taskColor )
        elif self.isOccupied( date ) is True:
            painter.fillRect( rect, self.occupiedColor )

        if date == QDate.currentDate():
            painter.drawRect( rect.left(), rect.top(), rect.width() - 1, rect.height() - 1 )

    def isHighlighted(self, date):
        if self.highlightModel is None:
            return False
        return self.highlightModel.isHighlighted( date )

    def isOccupied(self, date):
        if self.highlightModel is None:
            return False
        return self.highlightModel.isOccupied( date )

    def contextMenuEvent( self, event ):
        evPos     = event.pos()
        globalPos = self.mapToGlobal( evPos )
        tabPos    = self.cellsTable.mapFromGlobal( globalPos )
        cellIndex = self.cellsTable.indexAt( tabPos )
        if cellIndex.row() < 1:
            ## skip row with days of week
            return
        if cellIndex.column() < 1:
            ## skip column with number of week
            return

        contextMenu = QMenu(self)
        addTaskAction  = contextMenu.addAction("Nuevo Proyecto")
        action = contextMenu.exec_( globalPos )

        if action == addTaskAction:
            dayIndex = (cellIndex.row() - 1) * 7 + (cellIndex.column() - 1)
            contextDate = self.dateAt( dayIndex )
            self.addTask.emit( contextDate )

    def dateAt( self, dayIndex ):
        prevMonthDays = self.daysFromPreviousMonth()
        dayOffset = dayIndex - prevMonthDays
        currYear  = self.yearShown()
        currMonth = self.monthShown()
        currDate  = QDate( currYear, currMonth, 1 )
        return currDate.addDays( dayOffset )

    def daysFromPreviousMonth( self ):
        currYear     = self.yearShown()
        currMonth    = self.monthShown()
        firstOfMonth = datetime.date( currYear, currMonth, 1 )
        days = firstOfMonth.weekday()
        if days == 0:                       # 0 means Monday
            days += 7                       # there is always one row
        return days
