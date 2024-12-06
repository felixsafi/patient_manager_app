from datetime import datetime

class Note:

    def __init__(self, note_number, text):
        self.note_number = note_number
        self.text = text
        self.timestamp = datetime.now()

    def update_note(self, text):
        """updates note text and timestamp"""
        self.text = text
        self.timestamp = datetime.now()
    
    def __eq__(self, other):
        """check if number and text are equal"""
        return (self.note_number == other.note_number) and (self.text == other.text)
    
    def __str__(self):
        return "code: %d, text: %s" % (self.note_number, self.text)
