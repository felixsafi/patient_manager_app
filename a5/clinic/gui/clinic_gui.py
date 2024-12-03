import sys
from clinic.controller import Controller #import the controller to the main window
from clinic.gui.login_gui import LoginGUI #Import the login GUI
from clinic.gui.main_menu_gui import MainMenuGUI #Import the main menu view
from clinic.gui.appointment_gui import AppointmentGUI #import the appointment page
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        #main window setup
        self.main_window_widget = QWidget() #Create a Qwiget to serve as main menu
        self.setCentralWidget(self.main_window_widget) #set to the main window widget object
        self.main_window_layout = QStackedLayout() #make a stacked layout for easy page switching w/ out new windows
        self.main_window_widget.setLayout(self.main_window_layout)

        #create a controller and login page instance
        self.controller = Controller(autosave=True) #create the controller
        self.login_gui = LoginGUI(self.controller) #create the login page
        self.main_window_layout.addWidget(self.login_gui)

        #create other pages and add them - initialize empty before access granted
        self.main_menu_gui = MainMenuGUI(self.controller)
        self.main_window_layout.addWidget(self.main_menu_gui)
        self.appointment_gui = AppointmentGUI(self.controller)
        self.main_window_layout.addWidget(self.appointment_gui)

        #connect window changing signals
        self.login_gui.login_success_signal.connect(self.run_main_menu_page) #page change on success login
        self.main_menu_gui.logout_signal.connect(self.run_login_page) #page change on success logout
        self.main_menu_gui.start_appoint_signal.connect(self.run_appointment_page) #page change to start appt
        self.appointment_gui.exit_appointment_signal.connect(self.run_main_menu_page) #page change on success exit appointment

        #main window styling


        self.main_window_layout.setCurrentWidget(self.login_gui) #open to login view on start up

    def run_login_page(self):
        self.setWindowTitle("Sign In Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.login_gui)
        self.adjustSize() #Adjust size to fit the widgets
    
    def run_main_menu_page(self):
        self.main_menu_gui.refresh_patient_list_signal.emit()
        self.setWindowTitle("Main Menu Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.main_menu_gui)
        self.adjustSize() #Adjust size to fit the widgets

    def run_appointment_page(self):
        self.setWindowTitle("Appointment Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.appointment_gui)
        self.adjustSize() #Adjust size to fit the widgets


def main():

    app = QApplication(sys.argv) #create the application so cli args can be passed
    window = ClinicGUI() #this will be the window for the app
    window.show() #show cause hidden by default
    app.exec() #start event loop

if __name__ == '__main__':
    main()
