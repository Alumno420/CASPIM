from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject


def get_label_url( url: str ):
    return "<a href=\"%s\">%s</a>" % (url, url)


def set_label_url( label: QtWidgets.QLabel, url: str ):
    htmlText = get_label_url(url)
    label.setText( htmlText )


def find_parent(widget: QObject, objectType ):
    if widget is None:
        return None
    widget = get_parent( widget )
    while widget is not None:
        if isinstance(widget, objectType):
            return widget
        widget = get_parent( widget )
    return None


def get_parent( widget: QObject ):
    if callable(widget.parent) is False:
        ## some objects has "parent" attribute instead of "parent" method
        ## e.g. matplotlib's NavigationToolbar
        return None
    return widget.parent()


def render_to_pixmap( widget: QtWidgets.QWidget, outputPath=None ):
    rectangle = widget.geometry()
    pixmap = QtGui.QPixmap( rectangle.size() )
    widget.render( pixmap, QtCore.QPoint(), QtGui.QRegion(rectangle) )
    if outputPath is not None:
        pixmap.save( outputPath )
    return pixmap
