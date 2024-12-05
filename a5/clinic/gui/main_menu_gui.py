from clinic.gui.main_menu_gui_controller import mmgController
from clinic.gui.patient_table_model import PatientTableModel #import the patient table model class
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt6.QtWidgets import (
        QVBoxLayout,
        QWidget,
        QLabel,
        QLineEdit,
        QTableView,
        QPushButton,
        QHBoxLayout,
)
class MainMenuGUI(QWidget):
        #class signals
        error_notification_signal = pyqtSignal(str) #for displaying an error message
        success_notification_signal = pyqtSignal(str) #for displaying a success op message

        refresh_patient_list_signal = pyqtSignal() #updates the table to refelect current data
        logout_signal = pyqtSignal()
        start_appoint_signal = pyqtSignal()

        logout_signal_internal = pyqtSignal() #signal to logout
        search_patients_signal = pyqtSignal(str) #searches for term entered, passes str search term
        create_update_patient_signal = pyqtSignal(bool) #open "editor"/"creator" by passing one of these as first arg
        done_create_update_signal = pyqtSignal(bool) #send False for cancel and True for save/create
        start_appoint_signal_internal = pyqtSignal() #signal to start appt w cur patient
        delete_patient_signal = pyqtSignal() #delete cur patient
        patient_selected_signal = pyqtSignal() #when a row with a patient is selected
        
        def __init__(self, controller):
                super().__init__()
                self.controller = controller #ref to controller
                self.create_layout() #set up the gui
                self.connect_active_elements() #set up active elements to emit correct signals
                self.viewController = mmgController(self) #create/initialize view controller class
                
        def create_layout(self):
                """Create the GUI for the Main Window"""

                MainMenuGUI_layout = QVBoxLayout() #Primary layout is VBox

                #top bar buttons
                top_bar_layout = QHBoxLayout()
                
                self.refresh_button = QPushButton("\u21BB") #refresh_button
                self.refresh_button.setToolTip("Refresh List: Implements Changes") #show tip when hovering on this
                self.refresh_button.setObjectName("regularButton") #use style from the clinic_gui
                top_bar_layout.addWidget(self.refresh_button)

                self.logout_button = QPushButton("Logout") #logout button
                self.logout_button.setObjectName("navBarTextButton") #use style from the clinic_gui
                top_bar_layout.addWidget(self.logout_button)

                MainMenuGUI_layout.addLayout(top_bar_layout)

                #heading and subheading
                mm_heading = QLabel("Patient Management Tools")
                mm_heading.setObjectName("Heading1") #use style from the clinic_gui

                subheading0 = QLabel("Highlight patient by clicking on the row")
                subheading0.setObjectName("Heading2") #use style from the clinic_gui

                subheading1 = QLabel("Click start appointment to view / edit their files")
                subheading1.setObjectName("Heading3") #use style from the clinic_gui 

                subheading2 = QLabel("Click update to display the editor - hit save or cancel when done making changes")
                subheading2.setObjectName("Heading3") #use style from the clinic_gui                  
                
                MainMenuGUI_layout.addWidget(mm_heading)
                MainMenuGUI_layout.addWidget(subheading0)
                MainMenuGUI_layout.addWidget(subheading1)
                MainMenuGUI_layout.addWidget(subheading2)

                #search bar
                search_bar_layout = QHBoxLayout() #horizontal layour for seach bar and button

                self.search_input = QLineEdit() #search field
                self.search_input.setPlaceholderText("Search for patient name...") #placeholder for search field
                self.search_input.setObjectName("bigTextField") #use style from the clinic_gui
                self.search_button = QPushButton("\u2315") #set to a search icon
                self.search_button.setToolTip("search for matching name: case sensative") #show tip when hovering on this
                self.search_button.setObjectName("iconButton") #use style from the clinic_gui
                search_bar_layout.addWidget(self.search_button)
                search_bar_layout.addWidget(self.search_input)
                MainMenuGUI_layout.addLayout(search_bar_layout)

                #patient function buttons, and add them to the layout
                patient_function_buttons_layout = QHBoxLayout()

                self.create_patient_button = QPushButton("Create Patient")
                self.update_patient_button = QPushButton("Update Patient")
                self.start_appointment_button = QPushButton("Start Appointment")
                self.delete_patient_button = QPushButton("Delete Patient")

                # for button in self.patient_function_buttons:

                patient_function_buttons_layout.addWidget(self.create_patient_button)
                patient_function_buttons_layout.addWidget(self.update_patient_button)
                patient_function_buttons_layout.addWidget(self.start_appointment_button)
                patient_function_buttons_layout.addWidget(self.delete_patient_button)

                MainMenuGUI_layout.addLayout(patient_function_buttons_layout)

                #create_update widgets
                save_cancel_layout = QHBoxLayout() #save and cancel buttons
                self.save_create_update_fields_button = QPushButton("Save")
                self.cancel_create_update_button = QPushButton("Cancel")

                save_cancel_layout.addWidget(self.save_create_update_fields_button)
                save_cancel_layout.addWidget(self.cancel_create_update_button)
                MainMenuGUI_layout.addLayout(save_cancel_layout)
                

                create_update_fields_layout = QHBoxLayout() #fields for updating or making a patient
                self.phn_input = QLineEdit() #phn field
                self.phn_input.setPlaceholderText("phn")
                self.name_input = QLineEdit() #name field
                
                self.name_input.setPlaceholderText("name")
                self.birthday_input = QLineEdit() #birthday
                self.birthday_input.setPlaceholderText("birthday")
                self.phone_input = QLineEdit() #search field
                self.phone_input.setPlaceholderText("phone")
                self.email_input = QLineEdit() #search field
                self.email_input.setPlaceholderText("email")
                self.address_input = QLineEdit() #search field
                self.address_input.setPlaceholderText("address")
                MainMenuGUI_layout.addLayout(create_update_fields_layout)

                create_update_fields_layout.addWidget(self.phn_input)
                create_update_fields_layout.addWidget(self.name_input)
                create_update_fields_layout.addWidget(self.birthday_input)
                create_update_fields_layout.addWidget(self.phone_input)
                create_update_fields_layout.addWidget(self.email_input)
                create_update_fields_layout.addWidget(self.address_input)


                # #patient table view
                self.patient_view = QTableView()
                self.patient_model = PatientTableModel(self.controller)
                self.patient_view.setModel(self.patient_model)  # Set the model

                self.patient_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)#can only select one row at a time
                self.patient_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)# highlights entire row when clicked
                self.patient_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)  # Make table read-only

                MainMenuGUI_layout.addWidget(self.patient_view) #add to main layout

                #set up the layout
                main_widget = QWidget() #Create class widgit
                main_widget.setLayout(MainMenuGUI_layout) #set it to layout created
                self.setLayout(MainMenuGUI_layout) #apply to class

        def connect_active_elements(self):
                self.logout_button.clicked.connect(lambda: self.logout_signal_internal.emit()) #lamda allows non bool signal type
                self.refresh_button.clicked.connect(lambda: self.refresh_patient_list_signal.emit())
                self.search_button.clicked.connect(lambda: self.search_patients_signal.emit(self.search_input.text()))
                self.create_patient_button.clicked.connect(lambda: self.create_update_patient_signal.emit(True))
                self.update_patient_button.clicked.connect(lambda: self.create_update_patient_signal.emit(False))
                self.delete_patient_button.clicked.connect(lambda: self.delete_patient_signal.emit())
                self.start_appointment_button.clicked.connect(lambda: self.start_appoint_signal_internal.emit())
                self.cancel_create_update_button.clicked.connect(lambda: self.done_create_update_signal.emit(False))
                self.save_create_update_fields_button.clicked.connect(lambda: self.done_create_update_signal.emit(True))
                self.patient_view.selectionModel().selectionChanged.connect(lambda: self.patient_selected_signal.emit())

#self.phn_input.text(), self.name_input.text(), self.birthday_input.text(), self.phone_input.text(), self.email_input.text(), self.adress_input.text()


# class PatientTableModel(QAbstractTableModel):
#     def __init__(self, data, headers, parent=None):
#         super().__init__(parent)s
#         self._data = data  # Data for the table (list of lists)
#         self._headers = headers  # Column headers (list of strings)

#     def rowCount(self, parent=None):
#         return len(self._data)  # Number of rows

#     def columnCount(self, parent=None):
#         return len(self._headers)  # Number of columns

#     def data(self, index, role):
#         if not index.isValid():
#             return None

#         if role == Qt.ItemDataRole.DisplayRole:
#             return self._data[index.row()][index.column()]  # Cell data

#     def headerData(self, section, orientation, role):
#         if (
#             orientation == Qt.Orientation.Horizontal
#             and role == Qt.ItemDataRole.DisplayRole
#         ):
#             return self._headers[section]  # Column header
#         return None

