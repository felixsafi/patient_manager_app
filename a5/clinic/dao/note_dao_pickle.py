from pickle import load, dump
from clinic.note import Note
import string
from collections import OrderedDict, Counter #for ordered dict
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
        self.num_of_notes = 0
        self.ordered_notes = OrderedDict() #empy ordered dictionary

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
                    self.ordered_notes = load(file)
                    self.num_of_notes = len(self.ordered_notes)
                    self.note_count = self.num_of_notes

                    check_for_valid_note_count = None
                    while check_for_valid_note_count is None:
                        check_for_valid_note_count = self.search_note(self.note_count)
                        self.note_count +=1
        except Exception as e:
            with open(self.file_path, 'wb') as file:
                dump(self.ordered_notes, file)

    def search_note(self, note_number):
        """return the value for the given note num or None if ivalid key"""
        return self.ordered_notes.get(note_number, None) 
    
    def create_note(self, text):
        """create note update counter"""
        self.note_count += 1
        self.num_of_notes += 1
        new_note = Note(self.note_count, text)
        self.ordered_notes[self.note_count] = new_note
        

        # save file after creating a new note
        if self.autosave:
            with open(self.file_path, 'wb') as file:
                dump(self.ordered_notes, file)

        return new_note

    def retrieve_notes(self, search_string):
        """return list of matching notes"""
        
        
        retrieved_notes_list = []

        for i in range(self.ordered_notes[]):
            if search_string in self.ordered_notes[i]:
                print("YIPPIE YIPPIEE")


        #search_lowercase = search_string.lower() #makes lowercase
        #matching_notes_list = [
        #    value
        #    for value in self.ordered_notes.values()
        #    if search_lowercase in value.get("text", "").lower()  # Adjust for correct attribute
        #]

        #return matching_notes_list

    def update_note(self, note_number, text):
        """update the note if possible"""
        existing_note = self.search_note(note_number)
        if existing_note is not None:
            #update each value
            existing_note.update_note(text)
            self.ordered_notes.move_to_end(note_number) #moves to end of list if updated        
            self.save_list()# save file after updating 
            return note_number
        else:
            return False
   
    def delete_note(self, note_number):
        """delete the note if possible"""
        element = self.search_note(note_number)
        if element:
            del self.ordered_notes[note_number]
            if self.autosave:
                self.save_list()
            self.num_of_notes -=1
            return True
        else:
            return False
    
    def list_notes(self):
        """return a list of all the notes"""
        return [value for value in self.ordered_notes.values()]
    
    def save_list(self):
        """saves"""
        if self.autosave:
                with open(self.file_path, 'wb') as file:
                    dump(self.ordered_notes, file)
                self.num_of_notes = len
    
    def common_words(self):
        combined_notes = " ".join(self.list_notes) #combine all strings of words
        combined_notes = combined_notes.lower().translate(str.maketrans("", "", string.punctuation))#normalize all strings of notes
        all_words = {word for word in combined_notes.split() if len(word) >= 4} #gets words of at least 4 letters
        word_counts = Counter(all_words) #counts num of each valud word occurance

        return [word for word, count in word_counts.most_common((self.num_of_notes // 4)*1)] 
