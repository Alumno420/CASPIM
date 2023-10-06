from PyQt5.QtCore import QSettings, QObject
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from caspim.gui.utils import get_parent



# pylint: disable=R0915,R0912
def load_state(window: QMainWindow, settings: QSettings):
    settings.beginGroup( window.objectName() )
    geometry = settings.value("geometry")
    state = settings.value("windowState")
    if geometry is not None:
        window.restoreGeometry( geometry )
    if state is not None:
        window.restoreState( state )
    settings.endGroup()

    ## store geometry of all widgets
    widgets = window.findChildren( QtWidgets.QWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        geometry = settings.value("geometry")
        if geometry is not None:
            w.restoreGeometry( geometry )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QSplitter )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        state = settings.value("widgetState")
        if state is not None:
            w.restoreState( state )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QCheckBox )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        state = settings.value("checkState")
        if state is not None:
            w.setCheckState( int(state) )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QSpinBox )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        state = settings.value("value")
        if state is not None:
            w.setValue( int(state) )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTabWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        state = settings.value("currentIndex")
        if state is not None:
            currIndex = int(state)
            w.setCurrentIndex( currIndex )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTableView )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        colsNum = 0
        wmodel = w.model()
        if wmodel is not None:
            colsNum = wmodel.columnCount()
        for c in range(0, colsNum):
            state = settings.value( "column" + str(c) )
            if state is not None:
                currWidth = int(state)
                w.setColumnWidth( c, currWidth )
        sortColumn = settings.value( "sortColumn" )
        sortOrder = settings.value( "sortOrder" )
        if sortColumn is not None and sortOrder is not None:
            w.sortByColumn( int(sortColumn), int(sortOrder) )
        stretchLast = settings.value( "stretchLast" )
        if stretchLast is not None:
            stretchLastValue = bool(stretchLast)
            header = w.horizontalHeader()
            header.setStretchLastSection( stretchLastValue )
            if stretchLastValue:
                colsNum = header.count()
                w.resizeColumnToContents( colsNum - 1 )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTableWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        colsNum = w.columnCount()
        for c in range(0, colsNum):
            state = settings.value( "column" + str(c) )
            if state is not None:
                currWidth = int(state)
                w.setColumnWidth( c, currWidth )
        sortColumn = settings.value( "sortColumn" )
        sortOrder = settings.value( "sortOrder" )
        if sortColumn is not None and sortOrder is not None:
            w.sortByColumn( int(sortColumn), int(sortOrder) )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTreeView )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        colsNum = w.header().count()
        for c in range(0, colsNum):
            state = settings.value( "column" + str(c) )
            if state is not None:
                currWidth = int(state)
                w.setColumnWidth( c, currWidth )
        sortColumn = settings.value( "sortColumn" )
        sortOrder = settings.value( "sortOrder" )
        if sortColumn is not None and sortOrder is not None:
            w.sortByColumn( int(sortColumn), int(sortOrder) )
        settings.endGroup()


def save_state(window: QMainWindow, settings: QSettings):
    settings.beginGroup( window.objectName() )
    settings.setValue("geometry", window.saveGeometry() )
    settings.setValue("windowState", window.saveState() )
    settings.endGroup()

    ## store geometry of all widgets
    widgets = window.findChildren( QtWidgets.QWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        settings.setValue("geometry", w.saveGeometry() )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QSplitter )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        settings.setValue("widgetState", w.saveState() )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QCheckBox )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        settings.setValue("checkState", w.checkState() )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QSpinBox )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        settings.setValue("value", w.value() )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTabWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        settings.setValue("currentIndex", w.currentIndex() )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTableView )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        colsNum = w.model().columnCount()
        for c in range(0, colsNum):
            settings.setValue( "column" + str(c), w.columnWidth(c) )
        header = w.horizontalHeader()
        sortColumn = header.sortIndicatorSection()
        settings.setValue( "sortColumn", sortColumn )
        sortOrder = header.sortIndicatorOrder()
        settings.setValue( "sortOrder", sortOrder )
        stretchLast = header.stretchLastSection()
        settings.setValue( "stretchLast", stretchLast )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTableWidget )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        colsNum = w.columnCount()
        for c in range(0, colsNum):
            settings.setValue( "column" + str(c), w.columnWidth(c) )
        header = w.horizontalHeader()
        sortColumn = header.sortIndicatorSection()
        settings.setValue( "sortColumn", sortColumn )
        sortOrder = header.sortIndicatorOrder()
        settings.setValue( "sortOrder", sortOrder )
        settings.endGroup()

    widgets = window.findChildren( QtWidgets.QTreeView )
    widgetsList = sort_widgets( widgets )
    for w, wKey in widgetsList:
        settings.beginGroup( wKey )
        header = w.header()
        colsNum = header.count()
        for c in range(0, colsNum):
            settings.setValue( "column" + str(c), w.columnWidth(c) )
        sortColumn = header.sortIndicatorSection()
        settings.setValue( "sortColumn", sortColumn )
        sortOrder = header.sortIndicatorOrder()
        settings.setValue( "sortOrder", sortOrder )
        settings.endGroup()


def find_sub_widgets( parent, childType ):
    widgets = parent.findChildren( childType )
    return sort_widgets( widgets )


## Returns children with deterministic order.
## Keeping order is important during load/save
## because otherwise it causes widgets to loose
## stored state
def sort_widgets( widgetsList ):
    retList = []
    for w in widgetsList:
        wKey = get_widget_key(w)
        if wKey is None:
            continue
        retList.append( (w, wKey) )
    ## sort by wKey
    retList.sort(key=lambda x: x[1])
    return retList


def get_widget_key(widget: QObject, suffix=None ):
    if widget is None:
        return None
    retKey = None
    while widget is not None:
        if retKey is None:
            retKey = widget.objectName()
        else:
            retKey = widget.objectName() + "-" + retKey
        widget = get_parent( widget )
    if suffix is not None:
        retKey = retKey + "-" + suffix
    return retKey
