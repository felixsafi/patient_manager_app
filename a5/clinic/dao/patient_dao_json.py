import json
from clinic.patient import Patient
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class PatientDAOJSON(PatientDAO):

    def __init__(self, autosave = False):
        self.autosave = autosave

        #info for accessing files
        self.filename = "clinic/patients.json"

        self.current_patient = None
        self.patients = None

        # create empty list of patients or previously created patients with autosave on
        if self.autosave:
            try:
                with open(self.filename, 'r') as file:
                #open in read mode
                    clean_file = file.read().strip() #clean whitespace
                    self.patients = json.loads(clean_file, cls=PatientDecoder) if clean_file else []
                    #check to see if theres anything in the file and make empty list if nothing S
            except FileNotFoundError:
                self.patients = [] #no file exists make an empty list
        else:
            self.patients = [] #else anything else occurs start with empty list


    def search_patient(self, key):
        """search for a patient and return them if they exist"""
        #nordered list requests a search
        if self.patients is None:
            return None
        for element in self.patients:
            if (element.phn == key):
                return element
        return None
    
    def create_patient(self, patient):
        """create a patient if possible"""
        if self.search_patient(patient.phn) is None:
            self.patients.append(patient)
            # save file after creating patient
            if self.autosave:
                with open(self.filename, 'w') as file:
                    json.dump(self.patients, file, cls=PatientEncoder)
            return patient
        else:
            raise IllegalOperationException

    def retrieve_patients(self, search_string):
        retrieved = []
        if self.patients is not None:
            for element in self.patients:
                if search_string in element.name:
                    retrieved.append(element)
            return retrieved
        else:
            return []

    def update_patient(self, key, patient):
        """update patient if possible"""
        patient_to_update = self.search_patient(key)

        if (patient_to_update is None):
        #trying to update a non-existent patient
            raise IllegalOperationException()
        if (self.current_patient is not None) and (patient_to_update == self.current_patient):
        #trying to update the current patient
            raise IllegalOperationException()
        if (patient.phn!=key) and (self.search_patient(patient.phn) is not None):
        #trying to update to a taken phn
            raise IllegalOperationException()

        #update each value
        patient_to_update.phn = patient.phn
        patient_to_update.name = patient.name
        patient_to_update.birth_date = patient.birth_date
        patient_to_update.phone = patient.phone
        patient_to_update.email = patient.email
        patient_to_update.address = patient.address
        
        # save file after updating patient
        if self.autosave:
            with open(self.filename, 'w') as file:
                json.dump(self.patients, file, cls=PatientEncoder)
        
        return True
   
    def delete_patient(self, key):
        """remove a patient from the list if possible"""
        patient_to_delete = self.search_patient(key)

        if (patient_to_delete is None):
        #trying to delete a non-existent patient
            raise IllegalOperationException()
        if (self.current_patient is not None) and (patient_to_delete == self.current_patient):
        #trying to delete the current patient
            raise IllegalOperationException() 

        else:
            self.patients.remove(patient_to_delete)
            # save file after deleting patient
            if self.autosave:
                with open(self.filename, 'w') as file:
                    json.dump(self.patients, file, cls=PatientEncoder)
            return True
        
    def delete_all_patients(self):
        self.patients = []

        if self.autosave:
            with open(self.filename, 'w') as file:
                json.dump(self.patients, file, cls=PatientEncoder)

    def list_patients(self):
        """return a list of patients"""
        patients_list = []
        for patient in self.patients:
            patients_list.append(patient)
        return patients_list

    def get_current_patient(self):
        """return controllers current patient"""
        return self.current_patient

    def set_current_patient(self, phn):
        """sets passed patient to current patient"""
        self.current_patient = self.search_patient(phn)

        if (self.current_patient is None):
        #trying to set current patients a non-existent patient
            raise IllegalOperationException()

        return self.current_patient

    def unset_current_patient(self):
        """removes current pattient by setting current_patient to none"""
        self.current_patient = None