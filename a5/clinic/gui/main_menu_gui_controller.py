#imports to run the generate fake patients
import os
import stat

from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient
from clinic.gui import reset_pop_info

class mmgController():
    def __init__(self, main_menu_gui):
        self.mmg = main_menu_gui #ref to the main_menu_gui
        self.connect_signals() #connect signal to methods
        self.create_widgit_lists() #create lists for view controlling
        self.hide_show_buttons_for_update(False) #precautionary button hide reset on init
        self.new_patient_bool = True #true-create patient, false-update patient
        self.selected_patient = None #var for the currently selected patient
        self.ensure_valid_permissions

    def connect_signals(self):
        """connect button singals to correct methods"""
        self.mmg.logout_signal_internal.connect(self.logout)
        self.mmg.search_patients_signal.connect(self.search_patient)
        self.mmg.create_update_patient_signal.connect(self.create_update_cur_patient)
        self.mmg.done_create_update_signal.connect(self.save_cancel_create_update)
        self.mmg.delete_patient_signal.connect(self.delete_cur_patient)
        self.mmg.start_appoint_signal_internal.connect(self.start_appointment)
        self.mmg.refresh_patient_list_signal.connect(self.refresh_patient_list)
        self.mmg.patient_selected_signal.connect(self.set_selected_patient)
        self.mmg.populate_fake_patients_signal.connect(self.fake_patient_data)

    def logout(self):
        """logout and return to login window"""
        self.mmg.controller.logout()
        self.mmg.success_notification_signal.emit("you have been logged out successfully")
        self.mmg.logout_signal.emit()

    def update_field_change_forms(self, instruction_text):
        """updates placeholder text, and removes the old text"""
        new_field_texts = []
        if instruction_text == "selected":
            new_field_texts = [
                str(self.selected_patient.phn), 
                self.selected_patient.name, 
                self.selected_patient.birth_date,
                self.selected_patient.phone,
                self.selected_patient.email,
                self.selected_patient.address
                ]
        else:
            new_field_texts = ["phn", "name", "DD/MM/YYYY", "Phone Number", "Email", "Address"]

        i = 0
        for field in self.fields_to_change:
            field.setPlaceholderText(new_field_texts[i]) #set placeholder text to current string
            field.clear() #clear any old text that was left there
            i+=1


    def search_patient(self, search_text):
        """search for patient matching query entered"""
        self.refresh_patient_list(self.mmg.controller.retrieve_patients(search_text)) #returns list of patients

    def create_update_cur_patient(self, new_patient_bool):
        """
        opens the updater and hides other options until edit is saved of cancelled

        Args:
            new_patient_bool: true - create patient, false - not new patient (i.e update patient)
        """
        if new_patient_bool or (self.selected_patient is not None):
            if new_patient_bool: #update placeholder for making a new patient
                (self.update_field_change_forms("new"))
            else:  #update the placeholder text for updating an existing patient
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
                button.hide()
            for button in self.btns_to_enable_on_update:
                button.show()
        else: #hide/re-enable buttons after updating
            for button in self.btns_to_disable_on_update:
                button.show()
            for button in self.btns_to_enable_on_update:
                button.hide()        

    def save_cancel_create_update(self, update_create_saved_bool=False):
        """
        save the creation or patient update and
        Rehide and Enable buttons after the update is saved or cancelled
        
        args: 
            updated_create_saved_bool: true - save, false - cancel
        """
        

        if update_create_saved_bool:#update/create paitent and fill blanks with default values
            #make sure either blank or valid phn entered
            
            new_phn = self.mmg.phn_input.text() or (self.selected_patient.phn if (self.selected_patient is not None) else "") or (self.gen_new_phn())
            new_name = self.mmg.name_input.text() or (self.selected_patient.name if (self.selected_patient is not None) else "") or "no name provided"
            new_birth_date = self.mmg.birthday_input.text() or (self.selected_patient.birth_date if (self.selected_patient is not None) else "") or "00/00/0000"
            new_phone = self.mmg.phone_input.text() or (self.selected_patient.phone if (self.selected_patient is not None) else "") or "no phone provided"
            new_email = self.mmg.email_input.text() or (self.selected_patient.email if (self.selected_patient is not None) else "") or "no email provided"
            new_address = self.mmg.address_input.text() or (self.selected_patient.address if (self.selected_patient is not None) else "") or "no address provided"
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
        self.mmg.refresh_patient_list_signal.emit()

    def start_appointment(self):
        """start appointment"""
        try:
            if self.selected_patient is None:
                self.mmg.error_notification_signal.emit("please select a patient before starting an appointment")
            else:
                self.mmg.controller.set_current_patient(self.selected_patient.phn)
                self.mmg.success_notification_signal.emit(f"appointment started with {self.mmg.controller.get_current_patient().name}")
                self.mmg.start_appoint_signal.emit()
        except IllegalOperationException as e:
            self.mmg.error_notification_signal.emit("error: no patient selected for appointment")



    def delete_cur_patient(self):
        """delete the current selected patient and refresh the list"""
        try:
            if self.selected_patient is None:
                self.mmg.error_notification_signal.emit("please select a patient to delete")
            else:
                self.mmg.controller.delete_patient(self.selected_patient.phn)
                self.mmg.success_notification_signal.emit(f"{self.selected_patient.name} removed and list updated")
                self.mmg.refresh_patient_list_signal.emit()
        except IllegalOperationException as e:
            self.mmg.error_notification_signal.emit("error: no patient selected to delete")

    def set_selected_patient(self):
        """sets the highlighted row to cur patient"""
        
        # Get the selection model
        selected_patient_from_gui = self.mmg.patient_view.selectionModel().selectedRows()
        selected_row_num = selected_patient_from_gui[0].row()
        selected_phn = self.mmg.patient_model.index(selected_row_num, 0).data()  #get phn from that row
        self.selected_patient = self.mmg.controller.search_patient(selected_phn)

    def gen_new_phn(self):
        phn_length = 8 
        new_phn = len(self.mmg.controller.list_patients()) + 1 #start phn num at num patients + 1
        phn_found = False
        formatted_phn = int(f"{new_phn:0{phn_length}d}")

        counter = 0
        while phn_found == False: #while no available phn found    
            if self.mmg.controller.search_patient(formatted_phn) is None: #if phn available
                phn_found = True
            elif counter > 99999999:
                raise SufferingFromSuccess
            else: #if phn unavailable go to next num
                counter +=1
                new_phn += 1
                formatted_phn = f"{new_phn:0{phn_length}d}"
        
        return formatted_phn

    def refresh_patient_list(self, list_to_update_to=None):
        """updates to current list oF all patients or to a curated list if one is passeD"""
        self.mmg.patient_model.refresh_data() if list_to_update_to is None else self.mmg.patient_model.refresh_data(list_to_update_to)
        self.hide_show_buttons_for_update(False)

    def fake_patient_data(self, create_delete_bool=False):
        """"creates or removes fake patinets"""
        if create_delete_bool: 
            self.mmg.add_fake_patients.setEnabled(False)
            self.mmg.remove_fake_patients.setEnabled(True)
        else:
            self.mmg.add_fake_patients.setEnabled(True)
            self.mmg.remove_fake_patients.setEnabled(False)

        reset_pop_info.main(create_delete_bool, self.mmg.controller) #run create or remove
        self.mmg.success_notification_signal.emit("fake patients added/removed successfully")
        self.mmg.refresh_patient_list_signal.emit()

    def ensure_valid_permissions(self):
        """
        check for the add fake patients script and attempt to add them
        referenced: https://ismailtasdelen.medium.com/setting-chmod-value-with-python-7e14daaf09b3#:~:text=To%20set%20the%20permissions%20of,expressed%20as%20an%20octal%20number.&text=The%20octal%20number%200o644%20represents,rw%2Dr%2D%2Dr%2D%2D.
        """
        try: 
            self.mmg.add_fake_patients.setEnabled(True)
            self.mmg.remove_fake_patients.setEnabled(False)
            script_file = 'clinic/gui/reset_pop_info.py'
            script_file_exists = os.path.exists(script_file)
            if script_file_exists: # Check if the file is already executable and try to add permission if not
                current_permissions = os.stat("").st_mode #get cur permissions
                if not (current_permissions & stat.S_IXUSR):  # Check if user execute bit is set
                    # Add execute permissions for the user, group, and others
                    os.chmod(os.chmod("clinic/gui/reset_pop_info.py", stat.st_mode | stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR))
        except:
            self.mmg.error_notification_signal.emit("error loading the fake patients function - buttons disabled")
            self.mmg.add_fake_patients.setEnabled(False)
            self.mmg.remove_fake_patients.setEnabled(False)

class SufferingFromSuccess(Exception):
	''' Clinic doing too well, time to retire '''