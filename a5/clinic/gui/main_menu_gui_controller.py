from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient

class mmgController():
    def __init__(self, main_menu_gui):
        self.mmg = main_menu_gui #ref to the main_menu_gui
        self.connect_signals() #connect signal to methods
        self.create_widgit_lists() #create lists for buttons to show/hide for methods
        self.hide_show_buttons_for_update(False) #precautionary button hide reset on init
        self.new_patient_bool = True #true-create patient, false-update patient
        self.selected_patient = None #var for the currently selected patient

    def connect_signals(self):
        """connect button singals to correct methods"""
        self.mmg.logout_signal_internal.connect(self.logout)
        self.mmg.search_patients_signal.connect(self.search_patient)
        self.mmg.create_update_patient_signal.connect(self.create_update_cur_patient)
        self.mmg.done_create_update_signal.connect(self.save_cancel_create_update)
        self.mmg.delete_patient_signal.connect(self.delete_cur_patient)
        self.mmg.start_appoint_signal_internal.connect(self.start_appointment)
        self.mmg.refresh_patient_list_signal.connect(self.refresh_patient_list)

    def logout(self):
        """logout and return to login window"""
        self.mmg.controller.logout()
        self.mmg.success_notification_signal.emit("you have been logged out successfully")
        self.mmg.logout_signal.emit()

    def update_field_change_forms(self, instruction_text):
        """updates placeholder text"""
        new_field_texts = []
        if instruction_text == "selected":
            new_field_texts = [
                self.selected_patient.phn, 
                self.selected_patient.name, 
                self.selected_patient.birthday,
                self.selected_patient.phone,
                self.selected_patient.email,
                self.selected_patient.adress
                ]
        else:
            new_field_texts = ["phn", "name", "DD/MM/YYYY", "Phone Number", "Email", "Adress"]

        i = 0
        for field in self.fields_to_change:
            field.setPlaceholderText(new_field_texts[i])
            i+=1


    def search_patient(self, search_text):
        """search for patient matching query entered"""
        self.mmg.controller.retrieve_patients(search_text) #returns list of patients

    def create_update_cur_patient(self, new_patient_bool):
        """
        opens the updater and hides other options until edit is saved of cancelled

        Args:
            new_patient_bool: true - create patient, false - not new patient (i.e update patient)
        """
        self.set_selected_patient()
        if new_patient_bool or (self.selected_patient is not None):
            if new_patient_bool: #update placeholder for new patient or update patient
                (self.update_field_change_forms("new"))
            else: 
                (self.update_field_change_forms("selected"))

            self.hide_show_buttons_for_update(True) #show create/update buttons
            self.new_patient_bool = new_patient_bool #set to create or update
        else:
            self.mmg.error_notification_signal.emit("please select a patient to update")

    def create_widgit_lists(self):
        self.btns_to_disable_on_update = [  # buttons to disable while updating
                self.mmg.logout_button,
                self.mmg.create_patient_button,
                self.mmg.update_patient_button,
                self.mmg.start_appointment_button,
                self.mmg.delete_patient_button,
            ]

        self.btns_to_enable_on_update = [  # update related button to show
            self.mmg.save_create_update_fields_button,
            self.mmg.cancel_create_update_button,
            self.mmg.phn_input,
            self.mmg.name_input,
            self.mmg.birthday_input,
            self.mmg.phone_input,
            self.mmg.email_input,
            self.mmg.address_input,
        ]
        
        self.fields_to_change = [ #field with placeholder to change
            self.mmg.phn_input,
            self.mmg.name_input,
            self.mmg.birthday_input,
            self.mmg.phone_input,
            self.mmg.email_input,
            self.mmg.address_input,
        ]

    def hide_show_buttons_for_update(self, open_update_menu_bool):
        """
        hides/shows and disables/enables appropriate buttons for 
        starting/finishing updating a patient

        Args:
            open_update_menu_bool (bool): true - opens update menu, false-closes update menu
        """
        
        if open_update_menu_bool == True: #show/disable appropriate buttons to update/create a patient
            for button in self.btns_to_disable_on_update:
                button.setEnabled(False)
            for button in self.btns_to_enable_on_update:
                button.show()
        else: #hide/re-enable buttons after updating
            for button in self.btns_to_disable_on_update:
                button.setEnabled(True)
            for button in self.btns_to_enable_on_update:
                button.hide()        

    def save_cancel_create_update(self, update_create_saved_bool=False):
        """
        save the creation or patient update and
        Rehide and Enable buttons after the update is saved or cancelled
        
        args: 
            updated_create_saved_bool: true - save, false - cancel
        """
        if update_create_saved_bool :#update/create paitent and fill blanks with default values
            new_phn = self.mmg.phn_input.text() or (self.selected_patient.phn if (self.selected_patient is not None) else "") or (self.gen_new_phn())
            new_name = self.mmg.name_input.text() or (self.selected_patient.name if (self.selected_patient is not None) else "") or "no name provided"
            new_birth_date = self.mmg.birthday_input.text() or (self.selected_patient.birthday if (self.selected_patient is not None) else "") or "00/00/0000"
            new_phone = self.mmg.phone_input.text() or (self.selected_patient.phone if (self.selected_patient is not None) else "") or "no phone provided"
            new_email = self.mmg.email_input.text() or (self.selected_patient.email if (self.selected_patient is not None) else "") or "no email provided"
            new_address = self.mmg.address_input.text() or (self.selected_patient.text if (self.selected_patient is not None) else "") or "no adress provided"

            try:
                if self.new_patient_bool:
                    self.mmg.controller.create_patient(new_phn, new_name, new_birth_date, new_phone, new_email, new_address)
                else:
                    self.mmg.controller.update_patient(self.selected_patient.phn, new_phn, new_name, new_birth_date, new_phone, new_email, new_address)
                self.mmg.success_notification_signal.emit( 
                        f"saved {("the new" if self.new_patient_bool else "the update for")} " \
                        f" {("patient" if self.new_patient_bool else self.selected_patient.name)}"
                    )
            except IllegalOperationException as e: #emit error notification if using a taken phn
                self.mmg.error_notification_signal.emit( #inline if statements depend on if updating or creating
                    f"please enter an unused phn to {("update" if self.new_patient_bool else "create")}" \
                    f" {("new patient" if self.new_patient_bool else self.selected_patient.name)}"
                )
        else: #cancel the update or creation and submit a message
            self.mmg.success_notification_signal.emit( 
                f"cancelled patient {("creation" if self.new_patient_bool else "update")} for" \
                f" {("new patient" if self.new_patient_bool else self.selected_patient.name)}"
                )
        self.hide_show_buttons_for_update(False)
        self.update_field_change_forms("clear")

    def start_appointment(self):
        """start appointment"""
        # TODO 
        self.set_selected_patient()
        if self.selected_patient is None:
            self.mmg.error_notification_signal.emit("please select a patient before starting an appointment")
        else:
            self.mmg.controller.set_current_patient(1234567890)
            self.success_notification_signal.emit(f"appointment started {self.mmg.controller.get_current_patient.name()}")
            self.mmg.start_appoint_signal.emit()

    def delete_cur_patient(self):
        """delete the current selected patient and refresh the list"""
        self.set_selected_patient()
        if self.selected_patient is None:
            self.mmg.error_notification_signal.emit("please select a patient to delete")
        else:
            self.mmg.success_notification_signal.emit(f"{self.selected_patient.name} removed and list updated")
            self.mmg.controller.delete_patient(self.selected_patient_phn)
            self.mmg.refresh_patient_list_signal.emit()

    def set_selected_patient(self):
        """sets the highlighted row to cur patient"""
        
        # Get the selection model
        selection_model = self.mmg.patient_table_view.selectionModel()
        if selection_model.hasSelection():# check if row selected
            selected_row = self.mmg.patient_model.selectedRows()[0].row()  # Get the first selected row
            phn = self.patient_model.index(selected_row, 0).data()  #get phn from that row
            self.selected_patient = self.controller.search_patient(phn)
        else:
            print("No row selected")
            return None

    def gen_new_phn(self):
        phn_length = 8 
        new_phn = len(self.mmg.controller.list_patients) + 1 #start phn num at num patients + 1
        phn_found = False
        formatted_phn = f"{new_phn:0{phn_length}d}"

        counter = 0
        while phn_found == False: #while no available phn found    
            if self.controller.search_patient(formatted_phn) is None: #if phn available
                phn_found = True
            elif counter > 99999999:
                raise SufferingFromSuccess
            else: #if phn unavailable go to next num
                counter +=1
                new_phn += 1
                formatted_phn = f"{new_phn:0{phn_length}d}"

    def refresh_patient_list(self):
        self.mmg.patient_model.refresh_data()

class SufferingFromSuccess(Exception):
	''' Clinic doing to well, time to retire '''