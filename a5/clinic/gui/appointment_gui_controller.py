from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.note import Note
from collections import OrderedDict

class agController():
    def __init__(self, apointment_gui):
        self.ag = apointment_gui #ref to the gui
        self.controller = self.ag.controller #ref to the controller
        self.ag.notes_list = []
        self.notes_to_delete = []
        self.connect_signals()
        self.setUp()
    
    def connect_signals(self):
        """connect button singals to correct methods"""
        self.ag.search_notes_signal.connect(self.search_notes) #searches for term entered, passes str search term
        self.ag.save_all_notes_signal.connect(self.save_edits_deletes)  #saves edits if made
        self.ag.delete_note_signal.connect(self.delete_note) #delete cur note
        self.ag.list_notes_signal.connect(self.list_all) #refreshes all notes, updates view to ALL existing notes
        self.ag.update_search_signal.connect(self.search_notes) #search for notes
        #self.ag.create_note_signal.connect(self.create_note) #

    def setUp(self, passed_list=[-1]):
        if passed_list == [-1]: #not list passed
            self.ag.notes_list = self.get_notes_from_file
        else:
            self.ag.notes_list = passed_list

    def get_notes_from_file(self):
        if self.controller.login_status and self.controller.get_current_patient() is not None: #skip dynamic set up on initial creating to prevent error
                self.ag.notes_list = self.controller.list_notes()
        else: #set to default at the start
                self.ag.error_notification_signal("error loading notes from file")

    def list_all(self):
        """refresh view and unpdate to the current list of notes"""
        self.setUp()
        self.ag.create_notes_view()

    def search_notes(self, search_text):
        self.ag.notes_list = self.controller.retrieve_notes(search_text)
        self.setUp(self.ag.notes_list)
        self.ag.create_notes_view()

    def save_edits_deletes(self):
        """
        Save any changes made to the notes.

        Updates only the edited notes in the backend.
        """

        for note_to_delete in self.notes_to_delete: #remove notes in delete que
                    self.controller.delete_note(note_to_delete) #remove from backend

        self.get_notes_from_file #update to get notes list without deleted notes

        for note in self.ag.notes_list: #update all changed notes
            note_editor = self.ag.get_edit_window(f"note_text_at({note.note_number})")
            entered_text = note_editor.toPlainText() #normalize text from editor
            if note.text != entered_text:
                 self.controller.update_note(note.note_number, entered_text)
        
        self.list_all
            
    def delete_note(self, note_num_to_delete):
        """Delete note given key, refresh the view"""
        self.ag.sender().hide() #remove delete button after pressing
        self.notes_to_delete.append(note_num_to_delete)

    def create_note(self, new_note_text="nothing was entered for the note"):
        self.controller.create_note(new_note_text)
        self.list_all
