from clinic.gui.main_menu_gui_controller import mmgController
from clinic.gui.patient_table_model import PatientTableModel
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt6.QtWidgets import (
        QVBoxLayout,
        QWidget,
        QLabel,
        QLineEdit,
        QTableView,
        QPushButton,
        QHBoxLayout,
        QSpacerItem,
        QSizePolicy,
)

class MainMenuGUI(QWidget):
        #class signals
        error_notification_signal = pyqtSignal(str)#for displaying an error message
        success_notification_signal = pyqtSignal(str)#for displaying a success op message

        refresh_patient_list_signal = pyqtSignal()#updates the table to refelect current data
        logout_signal = pyqtSignal()
        start_appoint_signal = pyqtSignal()

        logout_signal_internal = pyqtSignal()#signal to logout
        search_patients_signal = pyqtSignal(str)#searches for term entered, passes str search term
        create_update_patient_signal = pyqtSignal(bool)#open "editor"/"creator" by passing one of these as first arg
        done_create_update_signal = pyqtSignal(bool)#send False for cancel and True for save/create
        start_appoint_signal_internal = pyqtSignal()#signal to start appt w cur patient
        delete_patient_signal = pyqtSignal()#delete cur patient
        patient_selected_signal = pyqtSignal()#when a row with a patient is selected
        
        def __init__(self, controller):
                super().__init__()
                self.user = "1"
                self.controller = controller#set reference to controller
                self.create_layout()#set up the gui
                self.connect_active_elements()#set up active elements to emit correct signals
                self.viewController = mmgController(self)#create/initialize view controller class
                
        def create_layout(self):
                """Create the GUI for the Main Window"""

                MainMenuGUI_layout = QVBoxLayout()#Primary layout is VBox

                #top bar layout
                top_bar_layout = QHBoxLayout()

                #Logged in as label
                self.logged_in_label = QLabel(f"Logged in as: {self.user}")#label for logged-in user
                self.logged_in_label.setObjectName("h2")#use style from clinic_gui
                top_bar_layout.addWidget(self.logged_in_label, alignment=Qt.AlignmentFlag.AlignLeft)

                #Spacer to align buttons to the right
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                top_bar_layout.addWidget(spacer)

                #Refresh button
                self.refresh_button = QPushButton("\u21BB")#refresh button
                self.refresh_button.setToolTip("Refresh List: Implements Changes")#show tip when hovering
                self.refresh_button.setObjectName("nav")#style as a primary button
                self.refresh_button.setStyleSheet("font-size: 125;")
                self.refresh_button.setFixedSize(40, 40)#size
                top_bar_layout.addWidget(self.refresh_button)

                #Logout button
                self.logout_button = QPushButton("Logout")#logout button
                self.logout_button.setObjectName("nav")#style as a primary button
                self.logout_button.setFixedHeight(40)#ensure consistent height with refresh button
                top_bar_layout.addWidget(self.logout_button)

                MainMenuGUI_layout.addLayout(top_bar_layout)

                #heading and subheadings
                mm_heading = QLabel("Patient Management Tools")
                mm_heading.setObjectName("h1")#use style from clinic_gui

                subheading0 = QLabel("Highlight patient by clicking on the row")
                subheading0.setObjectName("h2")#use style from clinic_gui

                subheading1 = QLabel("Click start appointment to view / edit their files")
                subheading1.setObjectName("h3")#use style from clinic_gui

                subheading2 = QLabel("Click update to display the editor - hit save or cancel when done making changes")
                subheading2.setObjectName("h3")#use style from clinic_gui

                MainMenuGUI_layout.addWidget(mm_heading)
                MainMenuGUI_layout.addWidget(subheading0)
                MainMenuGUI_layout.addWidget(subheading1)
                MainMenuGUI_layout.addWidget(subheading2)

                #search bar
                search_bar_layout = QHBoxLayout()#horizontal layout for search bar and button

                self.search_input = QLineEdit()#search field
                self.search_input.setPlaceholderText("Search for patient name...")#placeholder for search field
                self.search_input.setObjectName("regular")#use style from clinic_gui
                self.search_button = QPushButton("\u2315")#search button with icon
                self.search_button.setToolTip("Search for matching name: Case-sensitive")#show tip when hovering
                self.search_button.setObjectName("primaryButton")#style as a primary button
                search_bar_layout.addWidget(self.search_button)
                search_bar_layout.addWidget(self.search_input)
                MainMenuGUI_layout.addLayout(search_bar_layout)

                #patient function buttons
                patient_function_buttons_layout = QHBoxLayout()

                self.create_patient_button = QPushButton("Create Patient")
                self.create_patient_button.setObjectName("primaryButton")

                self.update_patient_button = QPushButton("Update Patient")
                self.update_patient_button.setObjectName("primaryButton")

                self.start_appointment_button = QPushButton("Start Appointment")
                self.start_appointment_button.setObjectName("primaryButton")

                self.delete_patient_button = QPushButton("Delete Patient")
                self.delete_patient_button.setObjectName("primaryButton")

                patient_function_buttons_layout.addWidget(self.create_patient_button)
                patient_function_buttons_layout.addWidget(self.update_patient_button)
                patient_function_buttons_layout.addWidget(self.start_appointment_button)
                patient_function_buttons_layout.addWidget(self.delete_patient_button)

                MainMenuGUI_layout.addLayout(patient_function_buttons_layout)

                #create/update widgets
                save_cancel_layout = QHBoxLayout()#save and cancel buttons
                self.save_create_update_fields_button = QPushButton("Save")
                self.save_create_update_fields_button.setObjectName("primaryButton")

                self.cancel_create_update_button = QPushButton("Cancel")
                self.cancel_create_update_button.setObjectName("primaryButton")

                save_cancel_layout.addWidget(self.save_create_update_fields_button)
                save_cancel_layout.addWidget(self.cancel_create_update_button)
                MainMenuGUI_layout.addLayout(save_cancel_layout)

                create_update_fields_layout = QHBoxLayout()#fields for updating or making a patient
                self.phn_input = QLineEdit()#phn field
                self.phn_input.setPlaceholderText("PHN")
                self.phn_input.setObjectName("smallTextField")

                self.name_input = QLineEdit()#name field
                self.name_input.setPlaceholderText("Name")
                self.name_input.setObjectName("smallTextField")

                self.birthday_input = QLineEdit()#birthday field
                self.birthday_input.setPlaceholderText("Birthday")
                self.birthday_input.setObjectName("smallTextField")

                self.phone_input = QLineEdit()#phone field
                self.phone_input.setPlaceholderText("Phone")
                self.phone_input.setObjectName("smallTextField")

                self.email_input = QLineEdit()#email field
                self.email_input.setPlaceholderText("Email")
                self.email_input.setObjectName("smallTextField")

                self.address_input = QLineEdit()#address field
                self.address_input.setPlaceholderText("Address")
                self.address_input.setObjectName("smallTextField")

                create_update_fields_layout.addWidget(self.phn_input)
                create_update_fields_layout.addWidget(self.name_input)
                create_update_fields_layout.addWidget(self.birthday_input)
                create_update_fields_layout.addWidget(self.phone_input)
                create_update_fields_layout.addWidget(self.email_input)
                create_update_fields_layout.addWidget(self.address_input)

                MainMenuGUI_layout.addLayout(create_update_fields_layout)

                #patient table view
                self.patient_view = QTableView()
                self.patient_model = PatientTableModel(self.controller)
                self.patient_view.setModel(self.patient_model)

                self.patient_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)#can only select one row at a time
                self.patient_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)#highlights entire row when clicked
                self.patient_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)#make table read-only
                self.patient_view.setObjectName("dataTable")

                MainMenuGUI_layout.addWidget(self.patient_view)

                self.setLayout(MainMenuGUI_layout)#apply to class

        def connect_active_elements(self):
                self.logout_button.clicked.connect(lambda: self.logout_signal_internal.emit())#logout signal
                self.refresh_button.clicked.connect(lambda: self.refresh_patient_list_signal.emit())#refresh signal
                self.search_button.clicked.connect(lambda: self.search_patients_signal.emit(self.search_input.text()))#search signal
                self.create_patient_button.clicked.connect(lambda: self.create_update_patient_signal.emit(True))#create patient signal
                self.update_patient_button.clicked.connect(lambda: self.create_update_patient_signal.emit(False))#update patient signal
                self.delete_patient_button.clicked.connect(lambda: self.delete_patient_signal.emit())#delete patient signal
                self.start_appointment_button.clicked.connect(lambda: self.start_appoint_signal_internal.emit())#start appointment signal
                self.cancel_create_update_button.clicked.connect(lambda: self.done_create_update_signal.emit(False))#cancel signal
                self.save_create_update_fields_button.clicked.connect(lambda: self.done_create_update_signal.emit(True))#save signal
                self.patient_view.selectionModel().selectionChanged.connect(lambda: self.patient_selected_signal.emit())#row selection signal