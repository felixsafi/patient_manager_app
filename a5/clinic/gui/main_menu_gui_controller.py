class mmgController():
    def __init__(self, main_menu_gui):
        self.mmg = main_menu_gui
        self.connect_signals()

    def connect_signals(self):
        print("running connect signals")
        self.mmg.logout_signal_internal.connect(self.logout)
        self.mmg.search_patients_signal.connect(self.search_patient)
        self.mmg.create_update_patient_signal.connect(self.create_update_cur_patient)
        self.mmg.done_create_update_signal.connect(self.save_cancel_create_update)
        self.mmg.delete_patient_signal.connect(self.delete_cur_patient)

    def logout(self):
        """logout and return to login window"""
        self.mmg.controller.logout()
        self.mmg.logout_signal.emit()

    def search_patient(self, search_text):
        """search for patient matching query entered"""
        self.mmg.controller.retrieve_patients(search_text) #returns list of patients

    def create_update_cur_patient(self):
        """opens the updater and hides other options until edit is saved of cancelled"""
        self.btns_to_disable_on_update = [  # buttons to disable while updating
            self.mmg.logout_button,
            self.mmg.create_patient_button,
            self.mmg.update_patient_button,
            self.mmg.start_appointment_button,
            self.mmg.delete_patient_button,
        ]

        self.btns_to_enable_on_update = [  # update related button to show
            self.mmg.save_create_update_fields_button,
            self.mmg.cancel_create_update_button
        ]

        for button in self.btns_to_disable:
            button.setEnabled(False)

        for button in self.btns_to_enable_on_update:
            button.show()

        # TODO Logic for updating patient

    def save_cancel_create_update(self, save_cancel_bool):
        """Rehide and Enable buttons after the update is saved or cancelled"""
        for button in self.btns_to_disable:
            button.setEnabled(True)
        for button in self.btns_to_enable_on_update:
            button.hide()

    def start_appointment(self):
        """start appointment"""
        # TODO add notification if no current patient selected and change to take cur patient
        self.controller.set_current_patient(1234567890)
        self.start_appointment_signal.emit()

    def delete_cur_patient(self):
        """delete the current selected patient and refresh the list"""
        self.refresh_patient_list_signal.emit()

    def set_current_patient(self):
        """sets the highlighted row to cur patient"""
        pass

    def refresh_patient_list(self):
        """reloads all patients"""
        pass

    # def create_table_model(self):
    #     # Column headers
    #     headers = ["PHN", "Name", "Birthday", "Phone", "Email", "Adress"]

    #     # Sample data (you will replace this with data from your external source)
    #     patients_list = [
    #         ["Patient 1", "12345", "1980/01/01", "123-456-7890", "f", "f", "f"],
    #         ["Patient 2", "67890", "1990/05/15", "234-567-8901", "f", "f", "f"],
    #         ["Patient 3", "54321", "1975/08/25", "345-678-9012", "f", "f", "f"],
    #         ["Patient 4", "98765", "2000/12/30", "456-789-0123", "f", "f", "f"],
    #     ]

    #     # Create and return the model
    #     return patients_list, headers


