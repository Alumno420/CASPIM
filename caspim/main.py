import sys
import os

import argparse

from caspim.gui.main_window import MainWindow

from caspim.gui.qt import QApplication
from caspim.gui.sigint import setup_interrupt_handling
from caspim.gui.widget.menustyle import MenuStyle
from caspim.fqueue import put_to_queue

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor
from PyQt5 import QtWidgets


script_dir = os.path.dirname(__file__)
tmp_dir    = os.path.realpath( os.path.join( script_dir, os.pardir, os.pardir, 'tmp' ) )



def run_app( args ):
    ## GUI
    app = QApplication(sys.argv)
    app.setApplicationName("CASPIM")
    app.setOrganizationName("KS")
    ### app.setOrganizationDomain("www.my-org.com")
    app.setQuitOnLastWindowClosed( False )

    ## disable Alt key switching to application menu
    app.setStyle( MenuStyle() )

    custom_font = QFont("Terminal", 14) 
    app.setFont(custom_font)

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(52, 136, 248))
    dark_palette.setColor(QPalette.Base, QColor(60, 60, 60))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255,158,0))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(80, 80, 80))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(169, 169, 169))
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(169, 169, 169))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(169, 169, 169))
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    QApplication.setPalette(dark_palette)

    setup_interrupt_handling()

    window = MainWindow()
    if args.blocksave is True:
        window.disableSaving()
    window.loadSettings()
    window.loadData()

    if args.minimized is False:
        window.show()


    home_directory = os.path.expanduser( '~' )
    path1 = os.path.join( home_directory, 'AppData', 'Roaming', "KS")
    path2 = os.path.join( home_directory, 'AppData', 'Roaming', "KS", "CASPIM-data")
    exists = os.path.isdir(path2)
    if exists == False:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.setStyleSheet("QLabel{min-width:200 px;min-height:200 px; font-size: 10px;} QPushButton{ width:250px; font-size: 18px; }")

        error_msg = "No existe el directorio: \n" + path2
        error_dialog.showMessage(error_msg)
        error_msg = "Ese diderectorio se va a crear ahora para que se guarde su informacion. Ctrl+S chrashea si no existe ese dir."
        error_dialog.showMessage(error_msg)

        if os.path.isdir(path1) == False:
            os.mkdir(path1)
        if os.path.isdir(path2) == False:
            os.mkdir(path2)
        exists = os.path.isdir(path2)
        if exists == True:
            error_msg = "Directorio: " + path2 + " creado satisfactoriamente."
        else:
            error_msg = "Directorio: " + path2 + " no se pudo crear. Por favor, hagalo usted manualmente."

        error_dialog.showMessage(error_msg)

    exitCode = app.exec_()

    if exitCode == 0:
        window.saveAll()

    return exitCode


def create_parser( parser: argparse.ArgumentParser = None ):
    if parser is None:
        parser = argparse.ArgumentParser(description='caspim')
    parser.add_argument('--minimized', action='store_const', const=True, default=False, help='Start minimized' )
    parser.add_argument('--blocksave', '-bs', action='store_const', const=True, default=None, help='Block save data' )
    return parser


def start( args=None ):

    if args is None:
        parser = create_parser()
        args = parser.parse_args()

    exitCode = 1

    exitCode = run_app( args )

    return exitCode


def start_single( args=None ):
    ## check if instance already running    
    try:
        start( args )
    except SystemExit:
        ## already running
        pass


def main( args=None ):
    if len( sys.argv ) != 2:
        ## run as usual
        start_single( args )
        return


if __name__ == '__main__':
    main()
