from PyQt5.QtWidgets import QUndoCommand


class RenameNoteCommand( QUndoCommand ):

    def __init__(self, dataObject, fromTitle, toTitle, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.fromTitle = fromTitle
        self.toTitle   = toTitle

        self.setText( "Renombrar reflexion: " + self.fromTitle )

    def redo(self):
        self.domainModel.renameNote( self.fromTitle, self.toTitle )
        self.data.notesChanged.emit()

    def undo(self):
        self.domainModel.renameNote( self.toTitle, self.fromTitle )
        self.data.notesChanged.emit()
