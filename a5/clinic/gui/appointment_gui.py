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
        appointment_success_signal = pyqtSignal(str)
        appointment_error_signal = pyqtSignal(str)

        search_notes_signal = pyqtSignal(str)#searches for term entered, passes str search term
        save_notes_signal = pyqtSignal() #saves edits if made
        delete_note_signal = pyqtSignal()#delete cur note
        list_notes_signal = pyqtSignal()
        create_note_signal = pyqtSignal()

        def __init__(self, controller):
                super().__init__()
                self.note_inputs = {}
                self.controller = controller#set reference to controller
                self.current_patient = "patient name" #TODO get cur patient note name
                self.create_layout()#set up the gui
                self.connect_active_elements()#set up active elements to emit correct signals
                self.viewController = agController(self)#create/initialize view controller class

                self.notes = []
                self.common_words = []

                

        def create_layout(self):
                """Create the GUI for the appointment Window"""        
                appointmentGUI_layout = QVBoxLayout()  # Main vertical layout

                # Navigation bar
                nav_bar = QHBoxLayout()

                # Appointment label for logged-in user
                self.appointment_with_label = QLabel("Logged in")
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
                appointmentGUI_layout.addLayout(nav_bar)

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
                appointmentGUI_layout.addLayout(search_bar_layout)

                # Note management buttons
                note_function_buttons_layout = QHBoxLayout()

                self.create_note_button = QPushButton("Create Note")
                self.create_note_button.setObjectName("primaryButton")  # Style for primary button

                self.save_button = QPushButton("Save Note Changes")
                self.save_button.setObjectName("primaryButton")

                self.list_all_notes_button = QPushButton("Refresh")
                self.list_all_notes_button.setObjectName("primaryButton")

                # Add buttons to the layout
                note_function_buttons_layout.addWidget(self.create_note_button)
                note_function_buttons_layout.addWidget(self.save_button)
                note_function_buttons_layout.addWidget(self.list_all_notes_button)
                appointmentGUI_layout.addLayout(note_function_buttons_layout)

                # Notes display section
                notes_label = QLabel("Notes")
                notes_label.setObjectName("h1")  # Apply "h1" style
                notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                appointmentGUI_layout.addWidget(notes_label)

                self.notes_view = self.create_notes_view()
                appointmentGUI_layout.addWidget(self.notes_view)

                self.setLayout(appointmentGUI_layout)

        def connect_active_elements(self):
                #self.logout_button.clicked.connect(lambda: self.logout_signal_internal.emit())#logout signal
                #self.refresh_button.clicked.connect(lambda: self.refresh_note_list_signal.emit())#refresh signal
                self.return_button.clicked.connect(lambda: self.exit_appointment_signal.emit()) #exit back to main menu
                self.create_note_button.clicked.connect(lambda: self.create_note_signal.emit())
                self.list_all_notes_button.clicked.connect(lambda: self.list_notes_signal.emit())
                self.search_button.clicked.connect(lambda: self.search_notes_signal.emit(self.search_input.text()))
                self.save_button.clicked.connect(lambda: self.save_notes_signal.emit())

        def create_notes_view(self):
                """
                Create a styled, scrollable section for notes.
                """
                # Scroll area
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setStyleSheet("background-color: #f5f5f5; border: none;")

                # Container widget inside the scroll area
                container = QWidget()
                container_layout = QVBoxLayout(container)
                container_layout.setSpacing(10)

                # Add each note dynamically
                self.notes = []
                if self.controller.login_status:
                        self.notes = self.controller.list_notes()
                else:
                        self.notes = [(Note(1, "example note")), (Note("2", "example_note"))]
                        

                for Anote in self.notes:
                        # Note container
                        note_frame = QFrame()
                        note_frame.setStyleSheet("""
                                QFrame {
                                border: 1px solid #cccccc;
                                border-radius: 5px;
                                background-color: #ffffff;
                                padding: 10px;
                                }
                        """)
                        note_frame_layout = QHBoxLayout(note_frame)

                        # Note input (editable text)
                        note_input = QLineEdit(Anote.text)
                        note_input.setStyleSheet("""
                                QLineEdit {
                                border: 1px solid #dddddd;
                                border-radius: 3px;
                                padding: 5px;
                                font-size: 14px;
                                }
                                QLineEdit:focus {
                                border-color: #3399ff;
                                }
                        """)
                        self.note_inputs[Anote.note_number] = note_input  # Track QLineEdit by note ID
                        note_frame_layout.addWidget(note_input, stretch=1)

                        # Delete button
                        delete_button = QPushButton("🗑")  # Trash icon (Unicode)
                        delete_button.setStyleSheet("""
                                QPushButton {
                                background-color: transparent;
                                color: #e74c3c;
                                border: none;
                                font-size: 18px;
                                }
                                QPushButton:hover {
                                color: #c0392b;
                                }
                        """)
                        delete_button.clicked.connect(lambda _, nid=Anote.note_number: self.controller.delete_note(nid))
                        note_frame_layout.addWidget(delete_button)

                        # Add frame to the container layout
                        container_layout.addWidget(note_frame)

                # Spacer to push content to the top
                container_layout.addStretch()

                # Set container as the scroll area widget
                scroll_area.setWidget(container)

                return scroll_area