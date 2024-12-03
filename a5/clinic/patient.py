from clinic.patient_record import PatientRecord

class Patient:

    def __init__(self, phn, name, birth_date, phone, email, address):
        """create a patient with all fields provided"""
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        #self.patient_records = PatientRecord(self) # create patientRecords object for each new patientC
        

    def create_note(self, note_text):
        """create a note in the patient records"""
        return self.patient_records.create_note(note_text)

    def update_note(self, note_number, update_text):
        """update a note in the patient records"""
        return self.patient_records.update_note(note_number, update_text)

    def retrieve_notes(self, search_text):
        """retrieve a note in the patient records"""
        return self.patient_records.retrieve_notes(search_text)
    
    def delete_note(self, note_number):
        """delete a note in the patient records"""
        return self.patient_records.delete_note(note_number)

    def list_notes(self):
        """update a note in the patient records"""
        return self.patient_records.list_notes()
    
    def search_note(self, note_number):
        return self.patient_records.search_note(note_number)
 

    def __eq__(self, other):
        """check if all fields are equal"""
        return (
            (self.phn == other.phn)
            and (self.name == other.name)
            and (self.birth_date == other.birth_date)
            and (self.phone == other.phone)
            and (self.email == other.email)
            and (self.address == other.address)
        )

    def __str__(self):
        """return string with patient fields"""
        return (
            "phn: %d, name: %s, birth date: %s, phone: %s, email: %s, address: %s"
            % (
                self.phn,
                self.name,
                self.birth_date,
                self.phone,
                self.email,
                self.address,
            )
        )
