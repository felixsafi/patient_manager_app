import sys
from PyQt6.QtCore import Qt, QAbstractTableModel

from clinic.controller import Controller
from clinic.patient import Patient

from clinic.exception.illegal_access_exception import IllegalAccessException


class PatientTableModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = []
        self.refresh_data()

    def refresh_data(self):
        self._data = []
        # TODO: Call the controller.list_patients().
        # With the results, build a matrix as a list of lists.
        # Each patients uses a full row from the matrix.
        # Each column in a row stores the patient's fields.
        

        try:
            patients = self.controller.list_patients()
            print(patients)
        except IllegalAccessException as e:
            patients = []
        
        
        for patient in patients:
            print(patient.name)
            patientlist = []
            patientlist.append(patient.phn)
            patientlist.append(patient.name)
            patientlist.append(patient.birth_date)
            patientlist.append(patient.phone)
            patientlist.append(patient.email)
            patientlist.append(patient.address)
            self._data.append(patientlist)

        self._data = [
        ["12345", "Patient 1", "1980/01/01", "123-456-7890", "f", "f"],
        ["67890", "Patient 2", "1990/05/15", "234-567-8901", "f", "f"],
        ["54321", "Patient 3", "1975/08/25", "345-678-9012", "f", "f"],
        ["98765", "Patient 4", "2000/12/30", "456-789-0123", "f", "f"],
        ]


        # emit the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def reset(self):
        self._data = []
        # emit the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Perform per-type checks and render accordingly.
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['Personal Health Number', 'Name', 'Birth Date', 'Phone', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)
