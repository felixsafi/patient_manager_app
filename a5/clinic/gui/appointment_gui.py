import sys
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
class AppointmentGUI(QWidget):
    exit_appointment_signal = pyqtSignal(str)

    def __init__(self, controller):
            super().__init__()
            self.windowTitle = 'Appointment Window'
            self.controller = controller #ref to controller
            self.get_appointment_view()
    
    def get_appointment_view(self):
            appointmentGUI_layout = QVBoxLayout()

            #Logout Button
            exit_appointment_button = QPushButton("Exit Appointment")
            exit_appointment_button.setStyleSheet("padding-right: 0px; text-align: center; margin-left: 300px;")
            exit_appointment_button.clicked.connect(self.exit_appointment)
            appointmentGUI_layout.addWidget(exit_appointment_button)

            #set the layout
            widget = QWidget()
            widget.setLayout(appointmentGUI_layout)
            self.setLayout(appointmentGUI_layout)

    def exit_appointment(self):
            self.exit_appointment_signal.emit("exit appointment") 
