import sys
from clinic.exception.invalid_login_exception import InvalidLoginException

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import(
        QVBoxLayout,
        QLineEdit,
        QLabel,
        QWidget,
        QGridLayout,
        QPushButton,
)
class LoginGUI(QWidget):
        login_success_signal = pyqtSignal(str)
        login_failed_signal = pyqtSignal(str)

        def __init__(self, controller):
                super().__init__()
                self.controller = controller #ref to controller
                self.create_layout() #set up the gui

        def create_layout(self):
                loginGUI_layout = QVBoxLayout() #create a grid-style layout for the login page

                loginGUI_layout.setSpacing(20) #space out elements

                #Instructions Label
                instructions_label = QLabel("Welcome back! Log in to the clinic manager")
                instructions_label.setObjectName("h1") #use style from the clinic_gui
                
                #Create Username Field
                self.user_name_field = QLineEdit()
                self.user_name_field.setPlaceholderText("Username")
                self.user_name_field.setObjectName("regular") #use style from the clinic_gui

                #create password Field
                self.password_field = QLineEdit()
                self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
                self.password_field.setPlaceholderText("Password")
                self.password_field.setObjectName("regular")

                #create login Button
                login_button = QPushButton("Login to App")
                login_button.clicked.connect(self.attempt_login)
                login_button.setObjectName("primaryButton")
                
                #add items to the layout
                loginGUI_layout.addWidget(instructions_label)
                loginGUI_layout.addWidget(self.user_name_field)
                loginGUI_layout.addWidget(self.password_field)
                loginGUI_layout.addWidget(login_button)

                #set up the layout
                main_widget = QWidget() #Create class widgit
                main_widget.setLayout(loginGUI_layout) #set it to layout created
                self.setLayout(loginGUI_layout) #apply to class
        
        def attempt_login(self):
                #get the text from the login fields
                username = self.user_name_field.text()
                password = self.password_field.text()

                #clear fields
                self.user_name_field.clear()
                self.password_field.clear()

                try: #attempt to login
                        self.controller.login(username, password) #pass creds to controller to check
                        self.login_success_signal.emit("a") #if success
                
                except InvalidLoginException as e: #catch and deal with failed attempt
                        self.login_failed_signal.emit("Invalid Credentials Entered") #emit if wrong creds
                
                
