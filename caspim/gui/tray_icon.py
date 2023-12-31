from enum import Enum, unique

from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QBrush, QColor, QPen
from PyQt5.QtWidgets import QApplication
from .qt import qApp, QSystemTrayIcon, QMenu, QAction

@unique
class TrayIconTheme(Enum):
    WHITE         = 'calendar-white.png'
    BLACK         = 'calendar-black.png'
    BLACK_WHITE   = 'calendar-bw.png'

    @classmethod
    def findByName(cls, name):
        for item in cls:
            if item.name == name:
                return item
        return None

    @classmethod
    def indexOf(cls, key):
        index = 0
        for item in cls:
            if item == key:
                return index
            if item.name == key:
                return index
            index = index + 1
        return -1


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__(parent)

        self.activated.connect( self._iconActivated )

#         Define and add steps to work with the system tray icon
#         show - show window
#         hide - hide window
#         exit - exit from application
        self.toggle_window_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        self.toggle_window_action.triggered.connect( self._toggleParent )
        quit_action.triggered.connect( qApp.quit )

        tray_menu = QMenu()
        tray_menu.addAction( self.toggle_window_action )
        tray_menu.addAction( quit_action )
        self.setContextMenu( tray_menu )

    def displayMessage(self, message):
        timeout = 10000
        ## under xfce4 there is problem with balloon icon -- it changes tray icon, so
        ## it cannot be changed back to proper one. Workaround is to use NoIcon parameter
        self.showMessage("CASPIM", message, QSystemTrayIcon.NoIcon, timeout)

    def drawNumber( self, number, numColor=QColor("red") ):
        icon = self.icon()

        pixmap = icon.pixmap( 512, 512 )
        pixSize = pixmap.rect()

        painter = QPainter( pixmap )

        font = painter.font()
        font.setPixelSize( 256 + 128 )
        painter.setFont(font)

        path = QPainterPath()
        path.addText( 0, 0, font, str(number) )
        pathBBox = path.boundingRect()

        xOffset = ( pixSize.width() - pathBBox.width() ) / 2 - pathBBox.left()
        yOffset = ( pixSize.height() + pathBBox.height() ) / 2

        path.translate( xOffset, yOffset )

#         pathPen = QPen(QColor("black"))
        pathPen = QPen( QColor(0, 0, 0, 200) )
        pathPen.setWidth( 180 )
        painter.strokePath( path, pathPen )

        painter.fillPath( path, QBrush(numColor) )

        ## make number bolder
        pathPen = QPen( numColor )
        pathPen.setWidth( 20 )
        painter.strokePath( path, pathPen )

        painter.end()

        self.setIcon( QIcon( pixmap ) )

    def _iconActivated(self, reason):
#         print("tray clicked, reason:", reason)
        if reason == 3:
            ## clicked
            self._toggleParent()

    def _toggleParent(self):
        parent = self.parent()
        self.updateLabel()
        if parent.isHidden() is False:
            ## hide window
            parent.hide()
            return
        ## show
        if parent.isMinimized():
            parent.showNormal()
        else:
            parent.show()
        QApplication.setActiveWindow( parent )      ## fix for KDE

    def updateLabel(self):
        parent = self.parent()
        if parent.isHidden():
            self.toggle_window_action.setText("Show")
        else:
            self.toggle_window_action.setText("Hide")
