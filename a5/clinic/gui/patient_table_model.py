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

    def refresh_data(self, passed_list=None):
        self.beginResetModel()
        self._data = []
        # TODO: Call the controller.list_patients().
        # With the results, build a matrix as a list of lists.
        # Each patients uses a full row from the matrix.
        # Each column in a row stores the patient's fields.
        

        try:
            patients = self.controller.list_patients() if (passed_list is None) else passed_list
            # print(patients)
        except IllegalAccessException as e:
            patients = []
        
        
        for patient in patients:
            patientlist = []
            patientlist.append(patient.phn)
            patientlist.append(patient.name)
            patientlist.append(patient.birth_date)
            patientlist.append(patient.phone)
            patientlist.append(patient.email)
            patientlist.append(patient.address)
            self._data.append(patientlist)

        # emit the layoutChanged signal to alert the QTableView of model changes
        # self.layoutChanged.emit()
        self.endResetModel()

    def reset(self):
        self.beginResetModel()
        self._data = []
        # emit the layoutChanged signal to alert the QTableView of model changes
        # self.layoutChanged.emit()
        self.endResetModel()

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
