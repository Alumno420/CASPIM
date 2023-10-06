import os

try:
    from PyQt5 import uic
except ImportError:
    ### No module named <name>
    exit(1)


base_dir = os.path.dirname( __file__ )
MAIN_MODULE_DIR = os.path.abspath( os.path.join( base_dir, ".." ) )


def generate_ui_file_name(classFileName):
    commonPrefix = os.path.commonprefix( [classFileName, base_dir] )
    relativePath = os.path.relpath(classFileName, commonPrefix)
    nameTuple = os.path.splitext(relativePath)
    return nameTuple[0] + ".ui"


def load_ui(uiFilename):
    try:
        ui_path = os.path.join( MAIN_MODULE_DIR, "ui", uiFilename )
        return uic.loadUiType( ui_path )
    except Exception as e:
        print("Exception while loading UI file:", uiFilename, e)
        raise


def load_ui_from_class_name(uiFilename):
    ui_file = generate_ui_file_name(uiFilename)
    return load_ui( ui_file )


def printsyspath():
    import sys
    for p in sys.path:
        print( "path:", p )
