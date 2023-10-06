import copy

from ..qt import pyqtSignal
from .. import uiloader
from .. import tray_icon


class AppSettings():

    def __init__(self):
        self.trayIcon = tray_icon.TrayIconTheme.WHITE

    def loadSettings(self, settings):
        settings.beginGroup( "app_settings" )

        trayName = settings.value("trayIcon", None, type=str)
        self.trayIcon = tray_icon.TrayIconTheme.findByName( trayName )

        if self.trayIcon is None:
            self.trayIcon = tray_icon.TrayIconTheme.WHITE

        settings.endGroup()

    def saveSettings(self, settings):
        settings.beginGroup( "app_settings" )

        settings.setValue("trayIcon", self.trayIcon.name)

        settings.endGroup()


UiTargetClass, QtBaseClass = uiloader.load_ui_from_class_name( __file__ )



class SettingsDialog(QtBaseClass):           # type: ignore

    iconThemeChanged         = pyqtSignal( tray_icon.TrayIconTheme )

    def __init__(self, appSettings, parentWidget=None):
        super().__init__(parentWidget)
        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        if appSettings is not None:
            self.appSettings = copy.deepcopy( appSettings )
        else:
            self.appSettings = AppSettings()

def load_keys_to_dict(settings):
    state = dict()
    for key in settings.childKeys():
        value = settings.value(key, "", type=str)
        if value:
            # not empty
            state[ key ] = value
    return state
