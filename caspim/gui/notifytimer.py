from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from caspim.domainmodel.reminder import Notification


class NotificationTimer( QObject ):

    remindTask = pyqtSignal( Notification )

    def __init__( self, *args ):
        QObject.__init__( self, *args )
        self.timer = QTimer(self)
        self.notifs = list()
        self.nextNotif = None
        self.timer.timeout.connect( self.handleTimeout )

    def setNotifications(self, notifList):
        self.notifs = notifList
        self.processNotifs()

    def processNotifs(self):
        self.timer.stop()
        if len(self.notifs) < 1:
            self.nextNotif = None
            return
        self.nextNotif = self.notifs.pop(0)
        secs = self.nextNotif.remainingSeconds()
        if secs > 0:
            millis = secs * 1000
            self.timer.start( millis )
        else:
            self.handleTimeout()

    def handleTimeout(self):
        self.remindTask.emit( self.nextNotif )
        self.processNotifs()
