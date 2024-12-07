from clinic.gui.appointment_gui_controller import agController
from clinic.note import Note
from PyQt6.QtWidgets import (
        QVBoxLayout,
        QHBoxLayout,
        QWidget,
        QLabel,
        QLineEdit,
        QPlainTextEdit,
        QPushButton,
        QSpacerItem,
        QSizePolicy,
        QFrame,
        QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

class AppointmentGUI(QWidget):
        exit_appointment_signal = pyqtSignal()
        success_notification_signal = pyqtSignal(str) #returns error message
        error_notification_signal = pyqtSignal(str) #retruns messages for opertations complete

        update_search_signal = pyqtSignal(str)#searches for term entered
        save_all_notes_signal = pyqtSignal() #saves edits if made
        delete_note_signal = pyqtSignal(int) #delete cur note
        search_notes_signal = pyqtSignal(str)
        list_notes_signal = pyqtSignal() #update the view to list all notes
        create_note_signal = pyqtSignal(str) #notify that note was created (send note text)

        def __init__(self, controller):
                super().__init__()
                self.list_of_notes = [Note(0, "test"), Note(2, "test1")]
                self.edit_field_dictionary = {} #dictionary to reference the edit fields 
                self.delete_buttons_dictionary = {} #dict to references each new delete button added

                self.controller = controller#set reference to controller 
                self.viewController = agController(self)#create/initialize view controller class

                self.create_layout()#set up the gui
                self.connect_active_elements()#set up active elements to emit correct signals
                
        def create_layout(self):
                """Create the GUI for the appointment Window"""        
                self.appointmentGUI_layout = QVBoxLayout()  # Main vertical layout

                # Navigation bar
                nav_bar = QHBoxLayout()

                # Appointment label for logged-in user
                self.appointment_with_label = QLabel("appointment with: defualt")
                self.appointment_with_label.setObjectName("h2")  # Apply "h2" style
                nav_bar.addWidget(self.appointment_with_label, alignment=Qt.AlignmentFlag.AlignLeft)

                # Spacer for aligning the return button
                space_menu = QWidget()
                space_menu.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                nav_bar.addWidget(space_menu)

                # Return button
                self.return_button = QPushButton("Return to Main Window")
                self.return_button.setObjectName("nav")  # Apply "nav" style
                self.return_button.setFixedHeight(40)
                nav_bar.addWidget(self.return_button)
                self.appointmentGUI_layout.addLayout(nav_bar)

                # Search bar
                search_bar_layout = QHBoxLayout()
                self.search_input = QLineEdit()  # Search input field
                self.search_input.setPlaceholderText("Search notes...")
                self.search_input.setObjectName("regular")  # Apply "regular" style
                self.search_button = QPushButton("\u2315")  # Search button with a magnifying glass icon
                self.search_button.setToolTip("Search for matching text in notes")  # Tooltip for guidance
                self.search_button.setObjectName("primaryButton")  # Apply "primaryButton" style
                search_bar_layout.addWidget(self.search_input)
                search_bar_layout.addWidget(self.search_button)
                self.appointmentGUI_layout.addLayout(search_bar_layout)

                # Notes display section
                notes_label = QLabel("Patient Records")
                notes_label.setObjectName("h1")  # Apply "h1" style
                notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.appointmentGUI_layout.addWidget(notes_label)

                # Note management buttons
                note_function_buttons_layout = QHBoxLayout()

                self.create_note_button = QPushButton("Create Note")
                self.create_note_button.setObjectName("primaryButton")  # Style for primary button

                self.save_button = QPushButton("Save All Changes")
                self.save_button.setObjectName("primaryButton")

                self.list_all_notes_button = QPushButton("Refresh")
                self.list_all_notes_button.setObjectName("primaryButton")

                # Add buttons to the layout
                note_function_buttons_layout.addWidget(self.create_note_button)
                note_function_buttons_layout.addWidget(self.save_button)
                note_function_buttons_layout.addWidget(self.list_all_notes_button)
                self.appointmentGUI_layout.addLayout(note_function_buttons_layout)

                self.notes_view = self.create_notes_view()
                #self.appointmentGUI_layout.addWidget(self.notes_view)

                self.setLayout(self.appointmentGUI_layout)



        def connect_active_elements(self):
                #self.logout_button.clicked.connect(lambda: self.logout_signal_internal.emit())#logout signal
                #self.refresh_button.clicked.connect(lambda: self.refresh_note_list_signal.emit())#refresh signal
                self.return_button.clicked.connect(lambda: self.exit_appointment_signal.emit()) #exit back to main menu
                self.create_note_button.clicked.connect(lambda: self.create_note_signal.emit())
                self.list_all_notes_button.clicked.connect(lambda: self.list_notes_signal.emit())
                self.search_button.clicked.connect(lambda: self.search_notes_signal.emit(self.search_input.text()))
                self.save_button.clicked.connect(lambda: self.save_notes_signal.emit())

        def create_notes_view(self):
                """make a scrollable view area with notes added"""
                
                #scrolling_layout = QLabel("appointment with: defualt")

                scrolling_layout = QScrollArea() #scrollable section
                scrolling_layout.setWidgetResizable(True) #adjustable for adding many notes
                scrolling_layout.setObjectName("notesView") #name for styling purposes

                #main widg for the notes view section
                main_notes_obj = QWidget() #create widget object for the view
                main_notes_view = QVBoxLayout(main_notes_obj) 
                main_notes_view.setSpacing(40) #space out from other elements

                self.edit_field_dictionary.clear()
                self.delete_buttons_dictionary.clear()

                for each_note in self.list_of_notes: #for all notes in the list

                        cur_note_num = each_note.note_number

                        self.new_frame = QFrame() #frame for design
                        self.new_frame.setObjectName("noteBox")

                        #vertical holder for label, and actual note
                        individual_note_layout = QVBoxLayout(self.new_frame)                        

                        #header for note
                        note_header = QLabel(f"Note {cur_note_num} Last Edited: {each_note.timestamp}") 
                        note_header.setObjectName("h2") #style as h2
                        individual_note_layout.addWidget(note_header)

                        #horiz layout for note editor and buttons
                        note_and_button_layout = QHBoxLayout() 

                        self.edit_field_dictionary[cur_note_num] = QPlainTextEdit() #note editor
                        self.edit_field_dictionary[cur_note_num].setPlainText(each_note.text) #set text to be the note text
                        self.edit_field_dictionary[cur_note_num].setObjectName("regular") #make findable for controler
                        note_and_button_layout.addWidget(self.edit_field_dictionary[cur_note_num])

                        self.delete_buttons_dictionary[cur_note_num] = QPushButton("delete") #addbutton to dictionary at note_num
                        self.delete_buttons_dictionary[cur_note_num].setObjectName("primaryButton") #styling
                        self.delete_buttons_dictionary[cur_note_num].clicked.connect(lambda: self.delete_note_signal.emit(cur_note_num)) #sends delete signal with note number
                        note_and_button_layout.addWidget(self.delete_buttons_dictionary[cur_note_num]) #add to h layout

                        individual_note_layout.addLayout(note_and_button_layout)
                
                        main_notes_view.addWidget(self.new_frame) #adds the whole frame as widg w eveything in it

                
                main_notes_view.addStretch() #aligning

                scrolling_layout.setWidget(main_notes_obj) #set scrolling view to display all notes

                return scrolling_layout #returns scrolling layout with everything in it

        
        # def get_edit_window(self, identifier_num): 
        #         labels = self.findChildren(QLabel)
        #         for label in labels: #go through all qlabel objects
        #                 if label.text() == str(identifier_num): #Check if the label text matches any
        #                         parent_layout = label.parentWidget().layout() #Get the parent layout of the label
        #                         if parent_layout: #if it exists
        #                                 for i in range(parent_layout.count()): #go through all 
        #                                         widget = parent_layout.itemAt(i).widget()
        #                                         if isinstance(widget, QPlainTextEdit):
        #                                                 return widget #return matching plain text edit
        #         return None  # Return None if not found
        
        def update_view(self):
                self.appointmentGUI_layout.removeWidget(self.notes_view)
                self.appointmentGUI_layout.addWidget(self.create_notes_view())