from clinic.exception.illegal_operation_exception import IllegalOperationException

class agController():
    def __init__(self, apointment_gui):
        self.ag = apointment_gui #ref to the gui
        self.controller = self.ag.controller #ref to the controller
        self.connect_signals()
        self.og_notes = {}
    
    def connect_signals(self):
        """connect button singals to correct methods"""
        #self.ag.search_notes_signal.connect(self.search_notes) #searches for term entered, passes str search term
        self.ag.save_notes_signal.connect(self.save_edits)  #saves edits if made
        self.ag.delete_note_signal.connect(self.delete_note) #delete cur note
        self.ag.list_notes_signal.connect(self.refresh_notes)
        self.ag.create_note_signal.connect(self.create_note)
    
    

    def refresh_notes(self):
        """get notes from contoller and update the view"""
        self.ag.appointmentGUI_layout.removeWidget(self.ag.notes_view)
        self.ag.notes_view.deleteLater()

        # Create a new notes section and add it to the layout
        self.ag.notes_view = self.ag.create_notes_section()
        self.ag.appointmentGUI_layout.addWidget(self.ag.notes_view)

    def add_note_to_display(self, note):
        """
        Add note to the display
        """
        # Append the "Last Edited" line (non-editable)
        self.ag.notes_view.appendPlainText(f"Last Edited: {note.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        #display like 2024-12-05 21:14:11
        
        self.ag.notes_view.appendPlainText(note.text) #add note content
        self.ag.notes_view.appendPlainText("") #

    def save_edits(self):
        """
        Save any changes made to the notes.

        Updates only the edited notes in the backend.
        """
        try:
            notes = self.ag.notes_view.toPlainText().strip().split("\n\n")

            for i, content in enumerate(notes):
                if not content.strip():
                    continue

                # Extract note text (skip the "Last Edited" line)
                lines = content.split("\n")
                note_text = "\n".join(lines[1:])  # Skip the first line

                # Compare with the original note content
                note_number = i + 1
                original_text = self.og_notes.get(note_number)

                if note_text != original_text:
                    # Update the backend with the new content
                    self.ag.controller.update_note(note_number, note_text)

            # Reload notes after saving changes
            self.refresh_notes()

        except Exception as e:
            print(f"Error saving edits: {e}")

    def delete_note(self):
        """
        Delete the currently selected note.

        Deletes the note from the backend and refreshes the notes display.
        """
        try:
            cursor = self.ag.notes_view.textCursor()
            cursor.select(self.ag.QTextCursor.SelectionType.LineUnderCursor)
            selected_text = cursor.selectedText()

            if selected_text.startswith("Last Edited:"):
                note_index = cursor.blockNumber() // 3 + 1  # Adjust for blank lines
                self.ag.controller.delete_note(note_index)
                self.refresh_notes()

        except Exception as e:
            print(f"Error deleting note: {e}")

    def create_note(self):
        """
        Create a new note with default content and refresh the display.
        """
        try:
            new_note_text = "New note content..."
            self.ag.controller.create_note(new_note_text)
            self.refresh_notes()

        except Exception as e:
            print(f"Error creating note: {e}")