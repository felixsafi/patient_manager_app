from pickle import load, dump
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class NoteDAOPickle(NoteDAO):

    def __init__(self, autosave = False, phn=None):
        self.autosave = autosave
        self.phn = phn #set patient phn for records access

        self.file_path = None #file_path to file to be accessed
        self.note_count = 0
        self.notes = {}

        # create empty list of notes or previously created notes with autosave on
        if self.autosave:
            self.autosave_setup(self.phn)

    def autosave_setup(self, phn):
        """
        set up for memory vs autosave

        Returns:
            notes dictionary populated if autosave on and data exists
        """
        try:
            if phn is not None:
                #info for accessing files
                self.file_path = f"clinic/records/{phn}.dat" #set filename to the correct patient if one exists
                
                with open(self.file_path, 'rb') as file:
                    #set the notes dictionary and counter from the file
                    self.notes = load(file)
                    self.note_count = len(self.notes)
        except FileNotFoundError:
            #create notes in memory if file not found
            self.notes = {}

    def search_note(self, note_number):
        """return the value for the given note num or None if ivalid key"""
        return self.notes.get(note_number, None) 

    # def does_note_exist(self, note_number):
    #     """check if the note exists"""
    #     if self.notes[note_number] is not None:
    #         return True
    #     else:
    #         return False
    
    def create_note(self, text):
        """create note update counter"""
        self.note_count += 1
        new_note = Note(self.note_count, text)
        self.notes[self.note_count] = new_note

        # save file after creating a new note
        if self.autosave:
            with open(self.file_path, 'wb') as file:
                dump(self.notes, file)
        return new_note

    def retrieve_notes(self, search_string):
        """return list of notes"""
        retrieved = []
        for element in self.notes.values():
            #search for matching notes
            if search_string in element.text:
                retrieved.append(element)
        return retrieved

    def update_note(self, note_number, text):
        """update the note if possible"""
        existing_note = self.search_note(note_number)
        if existing_note is not None:
            #update each value
            existing_note.update_note(text)
            
            # save file after updating patient
            if self.autosave:
                with open(self.file_path, 'wb') as file:
                    dump(self.notes, file)
            return True
        else:
            return False
   
    def delete_note(self, note_number):
        """delete the note if possible"""
        element = self.search_note(note_number)
        if element:
            self.notes[note_number] = None
            # save file after deleting patient
            if self.autosave:
                with open(self.file_path, 'wb') as file:
                    dump(self.notes, file)
            return True
        else:
            return False
    
    def list_notes(self):
        """return a list of all the notes"""
        notes_retrieved_list = []
        for item in self.notes.keys():
            if (self.notes[item] is not None):
                notes_retrieved_list.append(self.notes[item])
        return list(reversed(notes_retrieved_list))