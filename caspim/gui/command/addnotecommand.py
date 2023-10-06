from PyQt5.QtWidgets import QUndoCommand



class AddNoteCommand( QUndoCommand ):

    def __init__(self, dataObject, newNoteTitle, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.newNoteTitle = newNoteTitle

        self.setText( "Nueva reflexion: " + newNoteTitle )

    def redo(self):
        self.domainModel.addNote( self.newNoteTitle, "" )
        self.data.notesChanged.emit()

    def undo(self):
        self.domainModel.removeNote( self.newNoteTitle )
        self.data.notesChanged.emit()
