from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, autosave=False, phn=0):
        """create a List of notes and counter for the num of notes on init"""
        self.phn = phn
        self.autosave = autosave
        self.noteDAO = NoteDAOPickle(self.autosave, self.phn)

    def create_note(self, note_text):
        """create a new note"""
        return self.noteDAO.create_note(note_text)
    
    def search_note(self, search_note_number):
        """search for a note by number"""
        return self.noteDAO.search_note(search_note_number)
         
    def retrieve_notes(self, search_text):
        """search for the term in notes list and return a list of matching notes"""
        return self.noteDAO.retrieve_notes(search_text)

    def update_note(self, note_number, update_text):
        """updates note if it exists"""
        return self.noteDAO.update_note(note_number, update_text)    

    def delete_note(self, note_number):
        """deletes note if it exists"""
        return self.noteDAO.delete_note(note_number)

    def list_notes(self):
        """list all valid notes and return"""
        return self.noteDAO.list_notes()
