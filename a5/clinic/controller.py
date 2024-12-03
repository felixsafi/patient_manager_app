from clinic.patient import *
from clinic.patient_record import PatientRecord
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import hashlib

#DECORATORS FOR EXCEPTION HANDLING
def login_required_dec(func):
    """
    run a given method if logged in

    Args:
        *args and **kwargs - placeholders for all types of input
        self - ref to the self of the controller class to acess object fields
    Returns:
        the calling functions output on success
    Raises:
        IllegalAccessException() if not logged in
    """
    def inner_wrapper(self, *args, **kwargs):
        if self.login_status != 1: #check to see if login req is met
            raise IllegalAccessException()
        else:#if logged in run function or next check
            return func(self, *args, **kwargs)
    return inner_wrapper  # return result of the inner wraper func

class Controller:
    def __init__(self, autosave=False):
        # read from users.txt file and store each user in self.users dict
        self.autosave = autosave #persistance on/off (bool)
        self.users_login_data_dict = self.get_login_info()

        self.login_status = 0 #login status tracker

        self.patientDAO = PatientDAOJSON(self.autosave) #create patientDAO and pass autosave
        self.current_patient = self.patientDAO.current_patient #set the current patient

        if not self.autosave:
        #create a dictionary of patient data by phn in memory if autosave is off
            self.patient_records_dict = {}
        else:
            self.patient_record = None
        
    #SIGN IN METHODS
    def login(self, user_entered, password_entered):
        """
        login the user and update logged in status if applicable

        Args:
            username (str)
            password (str)
        Returns:
            True on success
        Raises:
            invalid_login_exception() on false credentials
            DuplicateLoginException() on double login attempt
        """
        if self.login_status == 1: #exception if already logged in
            raise DuplicateLoginException()

        for users in self.users_login_data_dict:
            #check if login info matches a correct user
            if users == user_entered:
                hashed_password_entered = self.hash_text(password_entered) # hash password entered
                if hashed_password_entered == self.users_login_data_dict.get(user_entered):
                    self.login_status = 1
                    return True
        raise InvalidLoginException() #if false login info this will raise

    def logout(self):
        """
        logout user if not alreay logged out

        Returns:
            true on successful logout
        Raises:
            duplicate_login_exception if already logged in
        """
        if self.login_status == 0:
            raise InvalidLogoutException()
        self.login_status = 0
        return True

    def get_login_info(self):
        users = {}

        if self.autosave:
            with open('clinic/users.txt', 'r') as login_file:
                for line in login_file:
                    # Assuming each line is "username, hashed password"
                    username, password_hash = line.strip().split(',')
                    users[username] = password_hash
            return users
        else:
            users["user"] = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
            users["ali"] = "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810"
            users["kala"] = "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"

            return users

    def hash_text(self, plain_text_password):
        """turns plain text to hashed password"""
        encoded_pass = plain_text_password.encode('utf-8')     # encode plain_text_password
        hashed_pass = hashlib.sha256(encoded_pass)      # hash encoded_pass
        digested_pass = hashed_pass.hexdigest()       # Get digest of hashed_pass
        return digested_pass

    #PATIENTS METHODS
    @login_required_dec
    def search_patient(self, search_phn): 
        """
        Pass the phn to the DAO to search for the patient
        Args:
            search_phn - phn to search for
        Returns:
            patient (patient object): if found
            None: if the patient doesnt exists
        """

        return self.patientDAO.search_patient(search_phn)

    @login_required_dec
    def create_patient(self, phn, name, birth_date, phone, email, address):
        """
        Pass the update info to the DAO to create the patient

        Args:
            name, birthday,...,adress - fields to initialize the patient
        Returns:
            patient (patient object): if successfully created
        Raises:
            IllegalOperationException - if trying to create a patient with taken phn
        """
        try:
            new_patient = Patient(phn, name, birth_date, phone, email, address)
            return self.patientDAO.create_patient(new_patient)
        except IllegalOperationException as e:
            raise 

    @login_required_dec
    def retrieve_patients(self, name):
        """
        generates and returns a list of patients given a name

        Args:
            name - name to search for 
        Returns:
            Populated list of patients: if matching patients exist
            empty List []: If none match
        """
        return self.patientDAO.retrieve_patients(name)
    
    @login_required_dec
    def update_patient(self, original_phn, new_phn, new_name, new_birth_date, new_phone, new_email, new_address):
        """
        Pass the phn and fields to the DAO to update the patient

        Args:
            original phn - the patient to update
            new_phn - phn to update to
            new_name, new_birthday,...,new_adress - fields to update
        Returns:
            True: if update successful
        Raises:
            IllegalOperationException:
                - trying to update none-existen patient
                - if trying to update a phn to one thats taken
        """
        try:
            updated_patient = Patient(new_phn, new_name, new_birth_date, new_phone, new_email, new_address)
            return self.patientDAO.update_patient(original_phn, updated_patient)
        except IllegalOperationException as e:
            raise 
        
    @login_required_dec
    def delete_patient(self, phn):
        """
        Deletes a patient from the system if they exist and are not the current patient selected.
        
        Args:
            phn (str): The PHN of the patient to delete.
        Returns:
            bool: True if the patient was successfully deleted.
        Raises:
            IllegalOperationException: If the patient does not exist or cannot be deleted 
        """
        try:
            return self.patientDAO.delete_patient(phn)
        except IllegalOperationException as e:
            raise

    @login_required_dec
    def list_patients(self):
        """
        Retrieves and returns a list of all patients managed by the controller.
        
        Returns:
            List[Patient]: A list of all patient objects in the system.
        """
        return self.patientDAO.list_patients()

    @login_required_dec
    def get_current_patient(self):
        """
        Returns the controller's current patient

        Returns:
            Patient: The current patient object
        """
        return self.patientDAO.get_current_patient()

    @login_required_dec
    def set_current_patient(self, phn):
        """
        Sets the passed patient as the current patient
        
        Args:
            phn (str): The phn of the patient to set as current
        Returns:
            Patient: The newly set current patient
        Raises:
            IllegalOperationException: If the patient does not exist
        """
        try:
            self.current_patient = self.patientDAO.set_current_patient(phn)
            if self.autosave:
                #if autosave is enabled proceed to check the file for data 
                self.patient_record = PatientRecord(self.autosave, self.current_patient.phn)
            else:
                #if disabled call fxn to deal w it
                self.handle_autosave_disabled(phn)
        except IllegalOperationException as e:
            raise
        
        return self.current_patient
        
    @login_required_dec
    def unset_current_patient(self):
        """removes current pattient by setting current_patient to none"""
        self.current_patient = self.patientDAO.unset_current_patient()
        self.patient_record = None
        return self.current_patient

    #NOTES METHODS
    def handle_autosave_disabled(self, phn):
        """
        Handles cases where autosave is disabled and manages patient records
        
        Args:
            phn (str): The phn of the patient
        """
        if phn in self.patient_records_dict:
            #if records for the patient were already created use those
            self.patient_record = self.patient_records_dict[phn]
        else:
            #if no records were created yet add to the dict
            self.patient_record = PatientRecord(self.autosave, self.current_patient.phn)
            self.patient_records_dict[phn] = self.patient_record

    #@cur_patient_required_dec
    @login_required_dec
    def create_note(self, note_text):
        """
        Calls create note with the fields passed in patient's record
        
        Args:
            note_text (str): The text of the note to create
        Returns:
            bool: True if the note was created successfully
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.create_note(note_text)
        else: 
            raise NoCurrentPatientException 

    #@cur_patient_required_dec
    @login_required_dec
    def retrieve_notes(self, search_text):
        """
        Retrieves notes matching the search query
        
        Args:
            search_text (str): The text to search in the notes
        Returns:
            List[Note]: A list of matching notes
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.retrieve_notes(search_text)
        else: 
            raise NoCurrentPatientException 

    #@cur_patient_required_dec
    @login_required_dec
    def update_note(self, note_number, update_text):
        """
        Updates a given patient note
        
        Args:
            note_number (int): The note number to update
            update_text (str): The new text for the note
        Returns:
            bool: True if the note was updated successfully
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.update_note(note_number, update_text)
        else: 
            raise NoCurrentPatientException 

    #@cur_patient_required_dec
    @login_required_dec
    def delete_note(self, note_number):
        """
        Deletes the note if it exists
        
        Args:
            note_number (int): The note number to delete
        Returns:
            bool: True if the note was deleted successfully
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.delete_note(note_number)
        else: 
            raise NoCurrentPatientException 

    #@cur_patient_required_dec
    @login_required_dec
    def list_notes(self):
        """
        Returns a list of notes for a given patient
        
        Returns:
            List[Note]: A list of notes for the current patient
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.list_notes()
        else: 
            raise NoCurrentPatientException 
    
    #@cur_patient_required_dec
    @login_required_dec
    def search_note(self, note_number):
        """
        Returns a note given the note number
        
        Args:
            note_number (int): The note number to retrieve
        Returns:
            Note: The note matching the provided number
        Raises:
            NoCurrentPatientException: If no current patient is selected
        """
        if self.current_patient is not None:
            return self.patient_record.search_note(note_number)
        else: 
            raise NoCurrentPatientException 