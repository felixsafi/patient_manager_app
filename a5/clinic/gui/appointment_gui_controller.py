from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.note import Note

class agController():
    def __init__(self, apointment_gui):
        self.ag = apointment_gui #ref to the gui
        self.controller = self.ag.controller #ref to the controller
        self.notes_to_delete_que = []
        self.connect_signals()
        self.setUp()
    
    def connect_signals(self):
        """connect button singals to correct methods"""
        self.ag.search_notes_signal.connect(self.search_notes) #searches for term entered, passes str search term
        self.ag.save_all_notes_signal.connect(self.save_edits_deletes)  #saves edits if made
        self.ag.delete_note_signal.connect(self.que_delete_note) #delete cur note
        self.ag.list_notes_signal.connect(self.list_all) #refreshes all notes, updates view to ALL existing notes
        self.ag.update_search_signal.connect(self.search_notes) #search for notes
        #self.ag.create_note_signal.connect(self.create_note) #

    def setUp(self, passed_list=None):
        if passed_list is None: #no list passed
            self.get_notes_from_file()
        else:
            self.ag.list_of_notes = passed_list

    def get_notes_from_file(self):
        if self.controller.login_status == 1: #skip dynamic set up on initial creating to prevent error
                self.ag.list_of_notes = self.controller.list_notes()
        else:
            self.ag.list_of_notes = []
    
    def list_all(self):
        """refresh view and unpdate to the current list of notes"""
        self.setUp()
        for note in self.ag.list_of_notes:
            print(note)
        self.ag.update_view()

    def search_notes(self, search_text):
        self.ag.list_of_notes = self.controller.retrieve_notes(search_text)
        self.setUp(self.ag.list_of_notes)
        self.list_all()

    def save_edits_deletes(self):
        """
        Save any changes made to the notes.

        Updates only the edited notes in the backend.
        """

        for notes in self.notes_to_delete_que: #remove notes in delete que
                    self.controller.delete_note(notes) #remove from backend
                    self.delete_buttons_dictionary[notes].show()

        self.get_notes_from_file #update to get notes list without deleted notes

        for note in self.ag.list_of_notes: #update all changed notes
            note_editor = self.ag.edit_field_dictionary[note.note_number]
            entered_text = note_editor.toPlainText() #normalize text from editor
            if note.text != entered_text:
                self.controller.update_note(note.note_number, entered_text)
        if self.ag.new_note:
            self.ag.new_note=False
            self.ag.create_frame.hide()
            self.controller.create_note(self.ag.notes_to_create_edit_field.text())

        self.list_all
            
    def que_delete_note(self, note_num_to_delete):
        """Delete note given key, refresh the view"""
        print(f"deleting {note_num_to_delete}")
        self.ag.delete_buttons_dictionary[note_num_to_delete].hide()
        self.notes_to_delete_que.append(note_num_to_delete)

    def create_note(self, new_note_text="nothing was entered for the note"):
        self.list_all()
        self.ag.create_frame.show()
  