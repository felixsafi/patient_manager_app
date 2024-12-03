from json import JSONEncoder
from clinic.patient import Patient

class PatientEncoder(JSONEncoder):
    """encode data for JSON format"""
    def default(self, obj):
        if isinstance(obj, Patient):
            return {
                "__type__": "Patient",
                "phn": obj.phn,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone": obj.phone,
                "email": obj.email,
                "address": obj.address,
            }
        return super().default(obj)
