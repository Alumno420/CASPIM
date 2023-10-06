import copy

from PyQt5.QtWidgets import QUndoCommand

class RemoveNoteCommand( QUndoCommand ):

    def __init__(self, dataObject, noteTitle, parentCommand=None):
        super().__init__(parentCommand)

        self.data = dataObject
        self.domainModel = self.data.getManager()
        self.noteTitle = noteTitle
        self.notes = None

        self.setText( "Eliminar reflexion: " + self.noteTitle )

    def redo(self):
        notesDict = self.domainModel.getNotes()
        self.notes = copy.deepcopy( notesDict )
        self.domainModel.removeNote( self.noteTitle )
        self.data.notesChanged.emit()

    def undo(self):
        self.domainModel.setNotes( self.notes )
        self.data.notesChanged.emit()
