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

        #create style elements dictionaries
        self.create_style_dict(0.3) #pick from 0.1(small)->0.9(big)
    


        #connect notification signals
        # self.main_menu_gui.success_notification_signal
        # self.main_menu_gui.error_notification_signal
        # self.login_gui.login_failed_signal
        # self.appointment_success_notification_signal 
        #self.appointment_gui.error_notification_signal


        self.main_window_layout.setCurrentWidget(self.login_gui) #open to login view on start up

    def run_login_page(self):
        self.setWindowTitle("Sign In Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.login_gui)
        self.adjustSize() #Adjust size to fit the widgets
    
    def run_main_menu_page(self):
        self.main_menu_gui.refresh_patient_list_signal.emit()
        self.setWindowTitle("Main Menu Page") #Set main window title
        #set the user name that logged in
        self.main_menu_gui.logged_in_label.setText(f"<span style='color : {self.design_ref_dict["secondaryText"]};'>logged in as:</span> {self.login_gui.current_user_logged_in}") 
        self.controller.unset_current_patient() #remove cur patient at start for page to work
        self.main_window_layout.setCurrentWidget(self.main_menu_gui)
        self.resize(1000, 700) #Adjust size to fit the widgets

    def run_appointment_page(self):
        #set the user name that logged in
        self.appointment_gui.list_notes_signal.emit()
        self.appointment_gui.appointment_with_label.setText(f"<span style='color : {self.design_ref_dict["secondaryText"]};'>In appointment with: </span> {self.controller.get_current_patient().name}") 
        self.setWindowTitle("Appointment Page") #Set main window title
        self.main_window_layout.setCurrentWidget(self.appointment_gui)
        self.adjustSize() #Adjust size to fit the widgets

    def create_style_dict(self, size_scale):
        self.design_ref_dict = { 
            "offGrey": "#2C2C2C",
            "primaryBackgroundGrey": "#1A1A1A",

            "mainText": "#E8E8E8",
            "secondaryText": "#A8A8A8",

            "primaryButtonCol": "#0B6E5A",
            "primaryButtonHov": "#095C4C",
            "primaryButtonPress": "#073E35",

            "secondaryButtonCol": "#2B6A81",
            "secondaryButtonHov": "#235668",
            "secondaryButtonPress": "#1A4554",

            "navButtonCol": "#1E1E1E",
            "navButtonHov": "#353535",
            "navButtonPress": "#2A2A2A",
            "navButtonText": "#E0E0E0",

            "tableHeaderBg": "#252525",
            "tableHeaderText": "#E0E0E0",
            "tableBg": "#151515",
            "tableAltRowBg": "#202020",
            "tableText": "#E5E5E5",
            "tableGrid": "#2D2D2D",

            "primaryButtonFontSize": 14,
            "primaryButtonPadding": 10,

            "secondaryButtonFontSize": 14,
            "secondaryButtonPadding": 10,

            "base_padding": 8,
            "pad_increment_exponent": (1+size_scale),
            "base_font_size": 12,
            "font_increment_exponent": (1+size_scale*3),
        }

        #properties for the elements used in the gui
        self.element_properties_dict = {
            "h1Fontsize": self.font_factor(3),
            "h1Fontcolor": self.design_ref_dict["mainText"],
            "h1Padding": self.pad_factor(1.5),

            "h2Fontsize": self.font_factor(1.5),
            "h2Fontcolor": self.design_ref_dict["mainText"],
            "h2Padding": self.pad_factor(1.2),

            "h3Fontsize": self.font_factor(1.1),
            "h3Fontcolor": self.design_ref_dict["secondaryText"],
            "h3Padding": self.design_ref_dict["base_padding"],

            "regularLineEditFontSize": self.font_factor(1.5),
            "regularLineEditFontColor": self.design_ref_dict["secondaryText"],
            "regularLineEditPadding": self.pad_factor(1.5),

            "smallLineEditFontSize": self.font_factor(1),
            "smallLineEditFontColor": self.design_ref_dict["secondaryText"],
            "smallLineEditPadding": self.pad_factor(1.1),

            "primaryButtonFontSize": self.font_factor(1.6),
            "primaryButtonColor": self.design_ref_dict["navButtonCol"],
            "primaryButtonHover": self.design_ref_dict["navButtonHov"],
            "primaryButtonPressed": self.design_ref_dict["navButtonPress"],
            "primaryButtonPadding": self.pad_factor(1.7),

            "secondaryButtonFontSize": self.font_factor(1.4),
            "secondaryButtonColor": self.design_ref_dict["secondaryButtonCol"],
            "secondaryButtonHover": self.design_ref_dict["secondaryButtonHov"],
            "secondaryButtonPressed": self.design_ref_dict["secondaryButtonPress"],
            "secondaryButtonPadding": self.pad_factor(1.55),

            "navButtonFontSize": self.font_factor(1.7),
            "navButtonColor": self.design_ref_dict["navButtonCol"],
            "navButtonHover": self.design_ref_dict["navButtonHov"],
            "navButtonPressed": self.design_ref_dict["navButtonPress"],
            "navButtonPadding": self.pad_factor(1.8),

            "tableHeaderBg": "#1E1F37",
            "tableHeaderText": "#E8E8E8",
            "tableBg": "#14151F",
            "tableAltRowBg": "#191A26",
            "tableText": "#F0F0F0",
            "tableGrid": "#1A2E35",
            "scrollbarHandle": "#1A2E35",
            "scrollbarHandleHover": "#14242B"
        }

    def font_factor(self, scale_int):
        return (self.design_ref_dict["base_font_size"]+(self.design_ref_dict["font_increment_exponent"]) ** scale_int)
    
    def pad_factor(self, scale_int):
        return (self.design_ref_dict["base_padding"]+(self.design_ref_dict["font_increment_exponent"]) ** scale_int)
        
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
        QLineEdit#regular {{
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
        QPushButton#primaryButton{{
            font-size: {self.element_properties_dict["primaryButtonFontSize"]}px;
            background-color: {self.element_properties_dict["primaryButtonColor"]};
            color: {self.design_ref_dict["mainText"]};
            border-radius: 4px;
            padding: {self.element_properties_dict["primaryButtonPadding"]}px;
            border: none;
        }}
        QPushButton#primaryButton:hover{{
            background-color: {self.element_properties_dict["primaryButtonHover"]};
        }}
        QPushButton#primaryButton:pressed {{
            background-color: {self.element_properties_dict["primaryButtonPressed"]};
        }}

        QPushButton#secondaryButton{{
            font-size: {self.element_properties_dict["secondaryButtonFontSize"]}px;
            background-color: {self.element_properties_dict["secondaryButtonColor"]};
            color: {self.design_ref_dict["mainText"]};
            border-radius: 4px;
            padding: {self.element_properties_dict["secondaryButtonPadding"]}px;
            border: none;
        }}
        QPushButton#secondaryButton:hover{{
            background-color: {self.element_properties_dict["secondaryButtonHover"]};
        }}
        QPushButton#secondaryButton:pressed {{
            background-color: {self.element_properties_dict["secondaryButtonPressed"]};
        }}

        QPushButton#nav{{
            font-size: {self.element_properties_dict["navButtonFontSize"]}px;
            background-color: {self.element_properties_dict["navButtonColor"]};
            color: {self.design_ref_dict["mainText"]};
            border-radius: 4px;
            padding: {self.element_properties_dict["navButtonPadding"]}px;
            border: none;
        }}
        QPushButton#nav:hover{{
            background-color: {self.element_properties_dict["navButtonHover"]};
        }}
        QPushButton#nav:pressed {{
            background-color: {self.element_properties_dict["navButtonPressed"]};
        }}

        QTableView{{
            background-color: {self.element_properties_dict["tableBg"]};
            alternate-background-color: {self.element_properties_dict["tableAltRowBg"]};
            color: {self.element_properties_dict["tableText"]};
            gridline-color: {self.element_properties_dict["tableGrid"]};
            border: 1px solid {self.element_properties_dict["tableGrid"]};
        }}

        QHeaderView::section{{
            background-color: {self.element_properties_dict["tableHeaderBg"]};
            color: {self.element_properties_dict["tableHeaderText"]};
            font-weight: bold;
            border: 1px solid {self.element_properties_dict["tableGrid"]};
            padding: 5px;
        }}

        QScrollBar:vertical, QScrollBar:horizontal{{
            background-color: {self.element_properties_dict["tableBg"]};
            border: none;
            width: 10px;
            height: 10px;
        }}
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal{{
            background-color: {self.element_properties_dict["scrollbarHandle"]};
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover{{
            background-color: {self.element_properties_dict["scrollbarHandleHover"]};
        }}
        QScrollBar::add-line, QScrollBar::sub-line{{
            background: none;
        }}
        """

def main():

    app = QApplication(sys.argv) #create the application so cli args can be passed
    app.setFont(QFont("Arial"))
    window = ClinicGUI() #this will be the window for the app
    app.setStyleSheet(window.generate_stylesheet())
    window.show() #show cause hidden by default
    app.exec() #start event loop

if __name__ == '__main__':

    main()

 