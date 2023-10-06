from ..qt import QtWidgets

class MenuStyle(QtWidgets.QProxyStyle):

    def styleHint(self, stylehint, opt, widget, returnData):
        if stylehint == QtWidgets.QStyle.SH_MenuBar_AltKeyNavigation:
            ## disable Alt key switching to application menu
            return 0
        return super().styleHint(stylehint, opt, widget, returnData)
