import sys
from clinic.controller import Controller #import the controller to the main window
from clinic.gui.login_gui import LoginGUI #Import the login GUI
from clinic.gui.main_menu_gui import MainMenuGUI #Import the main menu view
from clinic.gui.appointment_gui import AppointmentGUI #import the appointment page
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
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

        #app style elements
        self.design_ref_dict = { 
            "offGrey": "#383838",
            "primaryBackgroundGrey": "#212121",

            "mainText": "#ECECEC",
            "secondaryText": "#B4B4B4",

            "primaryButtonCol": "#689553",
            "primaryButtonHov": "#517645",
            "primaryButtonPress": "#2B3E25",

            "base_padding": 8
        }

        #properties for the elements used in the gui
        self.element_properties_dict = {
            "h1Fontsize": 20,
            "h1Fontcolor": self.design_ref_dict["mainText"],
            "h1Padding": self.design_ref_dict["base_padding"] + 4,

            "h2Fontsize": 16,
            "h2Fontcolor": self.design_ref_dict["mainText"],
            "h2Padding": self.design_ref_dict["base_padding"] + 2,

            "h3Fontsize": 12,
            "h3Fontcolor": self.design_ref_dict["secondaryText"],
            "h3Padding": self.design_ref_dict["base_padding"],

            "regularLineEditFontSize": 14,
            "regularLineEditFontColor": self.design_ref_dict["secondaryText"],
            "regularLineEditPadding": self.design_ref_dict["base_padding"] + 6,

            "smallLineEditFontSize": 12,
            "smallLineEditFontColor": self.design_ref_dict["secondaryText"],
            "smallLineEditPadding": self.design_ref_dict["base_padding"],

            "primaryButtonFontSize": 14,
            "primaryButtonColor": self.design_ref_dict["primaryButtonCol"],
            "primaryButtonHover": self.design_ref_dict["primaryButtonHov"],
            "primaryButtonPressed": self.design_ref_dict["primaryButtonPress"],
            "primaryButtonPadding": self.design_ref_dict["base_padding"] + 4,
        }
        
        def generate_stylesheet(self):
            """Generates a stylesheet using the design reference and element properties."""
            return f"""
            /*Background*/
            QWidget {{
                background-color: {self.design_ref_dict["primaryBackgroundGrey"]};
                color: {self.design_ref_dict["mainText"]};
            }}

            /*Headings*/
            QLabel#h1 {{
                font-size: {self.element_properties_dict["h1Fontsize"]}px;
                color: {self.element_properties_dict["h1Fontcolor"]};
                padding: {self.element_properties_dict["h1Padding"]}px;
            }}
            QLabel#h2 {{
                font-size: {self.element_properties_dict["h2Fontsize"]}px;
                color: {self.element_properties_dict["h2Fontcolor"]};
                padding: {self.element_properties_dict["h2Padding"]}px;
            }}
            QLabel#h3 {{
                font-size: {self.element_properties_dict["h3Fontsize"]}px;
                color: {self.element_properties_dict["h3Fontcolor"]};
                padding: {self.element_properties_dict["h3Padding"]}px;
            }}

            /*Input Fields*/
            QLineEdit {{
                font-size: {self.element_properties_dict["regularLineEditFontSize"]}px;
                color: {self.element_properties_dict["regularLineEditFontColor"]};
                padding: {self.element_properties_dict["regularLineEditPadding"]}px;
                background-color: {self.design_ref_dict["offGrey"]};
                border: 1px solid {self.design_ref_dict["secondaryText"]};
                border-radius: 4px;
            }}
            QLineEdit#small {{
                font-size: {self.element_properties_dict["smallLineEditFontSize"]}px;
                color: {self.element_properties_dict["smallLineEditFontColor"]};
                padding: {self.element_properties_dict["smallLineEditPadding"]}px;
                background-color: {self.design_ref_dict["offGrey"]};
                border: 1px solid {self.design_ref_dict["secondaryText"]};
                border-radius: 4px;
            }}

            /*Buttons*/
            QPushButton #primaryButton{{
                font-size: {self.element_properties_dict["primaryButtonFontSize"]}px;
                background-color: {self.element_properties_dict["primaryButtonColor"]};
                color: {self.design_ref_dict["mainText"]};
                border-radius: 4px;
                padding: {self.element_properties_dict["primaryButtonPadding"]}px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.element_properties_dict["primaryButtonHover"]};
            }}
            QPushButton:pressed {{
                background-color: {self.element_properties_dict["primaryButtonPressed"]};
            }}
            """

        #connect notification signals
        #self.main_menu_gui.success_notification_signal
        #self.main_menu_gui.error_notification_signal
        #self.login_gui.login_failed_signal


        self.main_window_layout.setCurrentWidget(self.login_gui) #open to login view on start up

    def run_login_page(self):
        self.setWindowTitle("Sign In Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.login_gui)
        self.adjustSize() #Adjust size to fit the widgets
    
    def run_main_menu_page(self):
        self.main_menu_gui.refresh_patient_list_signal.emit()
        self.setWindowTitle("Main Menu Page") #Set main window title
        self.controller.unset_current_patient() #remove cur patient at start for page to work
        self.main_window_layout.setCurrentWidget(self.main_menu_gui)
        self.adjustSize() #Adjust size to fit the widgets

    def run_appointment_page(self):
        self.setWindowTitle("Appointment Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.appointment_gui)
        self.adjustSize() #Adjust size to fit the widgets


def main():

    app = QApplication(sys.argv) #create the application so cli args can be passed
    app.setFont(QFont("Arial"))
    window = ClinicGUI() #this will be the window for the app
    app.setStyleSheet(window.generate_stylesheet())
    window.show() #show cause hidden by default
    app.exec() #start event loop

if __name__ == '__main__':

    main()

 