#!/usr/bin/env python3
#clears all patients and records, then populates the files

import os
import sys
import random
from clinic.controller import Controller

class resetAndAddContent():
    def __init__(self, create_bool):
        self.controller = Controller(autosave=True)
        self.controller.login("user", "123456")

        self.clear_all_old_files()
        if (create_bool == 1): self.populate_table()

    def clear_all_old_files(self):
        patients_file = 'clinic/patients.json'
        patients_file_exists = os.path.exists(patients_file)
        records_path = 'clinic/records'
        if os.path.exists(records_path):
            filenames = os.listdir(records_path)
            for filename in filenames:
                record_file_path = os.path.join(records_path, filename)
                if os.path.isfile(record_file_path):
                    os.remove(record_file_path)
        # removing the patients file later to avoid concurrency issues
        if patients_file_exists:
            os.remove(patients_file)

    def populate_table(self):
        phns_list = [12345678, 87654321, 23456789, 98765432, 34567890, 76543210, 45678901, 65432109, 56789012, 54321098, 67890123, 43210987, 78901234, 32109876, 89012345, 21098765, 90123456, 10987654, 12349876, 87651234, 23456701, 98760123, 34560198, 76509876, 45671234, 65438901, 56789098, 54321789, 67891234, 43217654, 98765401, 12348765, 23456780, 87650987, 34569876, 76540123, 45678932, 65432087, 56789076, 54321980, 67890321, 43219876, 78901265, 32108976, 89013245, 21097654, 90124356, 10986543, 12347658, 87654320]
        names_list = ["Emma Harrison", "Liam Carter", "Olivia Mitchell", "Noah Bennett", "Ava Brooks", "Ethan Collins", "Sophia Morgan", "Mason Reed", "Isabella Cruz", "Logan Foster", "Mia Parker", "Lucas Rivera", "Charlotte Hayes", "Benjamin Scott", "Amelia Gray", "James Walker", "Harper Lewis", "Elijah Hill", "Evelyn Adams", "Henry Young", "Chloe Peterson", "Alexander Price", "Ella Martinez", "Daniel Cooper", "Grace Turner", "Michael Phillips", "Scarlett Evans", "William King", "Emily Torres", "Jack Fisher", "Lily Ross", "Aiden White", "Victoria Ward", "Samuel Hughes", "Zoe Murphy", "Sebastian Ramirez", "Hannah Kelly", "Matthew Flores", "Abigail Morris", "David Powell", "Aria Cook", "Joseph Sanders", "Natalie Morris", "Ryan Butler", "Layla Griffin", "Gabriel Ross", "Victoria Rivera", "Carter Hayes", "Avery Brooks", "Julian Scott"]
        birthdays_list = ["1995/06/15", "1988/11/23", "2002/03/19", "1990/08/10", "1985/12/30", "1999/04/07", "1992/09/25", "2001/02/14", "1987/07/13", "1993/01/22", "1996/10/05", "1998/05/18", "1984/03/09", "2000/12/11", "1991/08/31", "1994/04/27", "1986/06/09", "1997/11/03", "1989/02/20", "1995/09/06", "1990/01/30", "1988/07/19", "1993/05/25", "1992/10/02", "1994/12/15", "1991/06/28", "2002/08/17", "1987/09/22", "2000/03/05", "1999/11/08", "1998/01/19", "1997/12/14", "1989/04/12", "1995/05/10", "1986/10/21", "1996/08/03", "1990/07/30", "1991/09/12", "1994/03/26", "1987/11/07", "1993/06/24", "1992/02/28", "1988/09/11", "1999/12/04", "2001/07/09", "1998/05/21", "1985/11/18", "2000/06/02", "1997/01/08", "1994/10/27"]
        phone_numbers_list = ["123-456-7890", "987-654-3210", "234-567-8901", "876-543-2109", "345-678-9012", "765-432-1098", "456-789-0123", "654-321-0987", "567-890-1234", "543-210-9876", "678-901-2345", "432-109-8765", "789-012-3456", "321-098-7654", "890-123-4567", "210-987-6543", "901-234-5678", "109-876-5432", "123-498-7654", "876-512-3498", "234-567-8012", "987-601-2345", "345-601-9876", "765-098-7612", "456-712-3456", "654-389-0123", "567-890-9876", "543-217-8943", "678-912-3498", "432-176-5401", "987-654-0123", "123-487-6543", "234-567-8098", "876-509-8761", "345-698-7634", "765-401-2398", "456-789-3298", "654-320-8765", "567-890-7643", "543-219-8098", "678-903-2145", "432-198-7654", "789-012-6534", "321-089-7654", "890-132-4543", "210-976-5432", "901-243-5678", "109-865-4321", "123-476-5890", "876-543-2098"]
        emails_list = ["emma.harrison@example.com", "liam.carter@example.com", "olivia.mitchell@example.com", "noah.bennett@example.com", "ava.brooks@example.com", "ethan.collins@example.com", "sophia.morgan@example.com", "mason.reed@example.com", "isabella.cruz@example.com", "logan.foster@example.com", "mia.parker@example.com", "lucas.rivera@example.com", "charlotte.hayes@example.com", "benjamin.scott@example.com", "amelia.gray@example.com", "james.walker@example.com", "harper.lewis@example.com", "elijah.hill@example.com", "evelyn.adams@example.com", "henry.young@example.com", "chloe.peterson@example.com", "alexander.price@example.com", "ella.martinez@example.com", "daniel.cooper@example.com", "grace.turner@example.com", "michael.phillips@example.com", "scarlett.evans@example.com", "william.king@example.com", "emily.torres@example.com", "jack.fisher@example.com", "lily.ross@example.com", "aiden.white@example.com", "victoria.ward@example.com", "samuel.hughes@example.com", "zoe.murphy@example.com", "sebastian.ramirez@example.com", "hannah.kelly@example.com", "matthew.flores@example.com", "abigail.morris@example.com", "david.powell@example.com", "aria.cook@example.com", "joseph.sanders@example.com", "natalie.morris@example.com", "ryan.butler@example.com", "layla.griffin@example.com", "gabriel.ross@example.com", "victoria.rivera@example.com", "carter.hayes@example.com", "avery.brooks@example.com", "julian.scott@example.com"]
        adresses_list = ["123 Maple Street, Springfield, IL", "456 Oak Avenue, Denver, CO", "789 Pine Road, Austin, TX", "101 Birch Lane, Seattle, WA", "202 Elm Boulevard, Boston, MA", "303 Cedar Street, Orlando, FL", "404 Willow Way, Nashville, TN", "505 Cherry Circle, Atlanta, GA", "606 Walnut Drive, Dallas, TX", "707 Poplar Court, Phoenix, AZ", "808 Sycamore Place, Portland, OR", "909 Hickory Terrace, Miami, FL", "111 Ash Crescent, Houston, TX", "222 Redwood Path, Las Vegas, NV", "333 Spruce Parkway, San Diego, CA", "444 Aspen Trail, Minneapolis, MN", "555 Alder Alley, Kansas City, MO", "666 Magnolia Crossing, New Orleans, LA", "777 Dogwood Square, Pittsburgh, PA", "888 Cottonwood Loop, Sacramento, CA", "999 Chestnut Bend, Baltimore, MD", "1212 Juniper Hill, Charlotte, NC", "1313 Beechwood Valley, San Antonio, TX", "1414 Fir Grove, Cincinnati, OH", "1515 Cypress Row, Milwaukee, WI", "1616 Maplewood Heights, Denver, CO", "1717 Birchwood Manor, Raleigh, NC", "1818 Pinecone Meadow, Tucson, AZ", "1919 Elmwood Cove, Salt Lake City, UT", "2020 Redwood Glade, Indianapolis, IN", "2121 Sprucehaven Ridge, Oklahoma City, OK", "2222 Cedarstone Vista, Richmond, VA", "2323 Willowcreek Point, Portland, ME", "2424 Hickorytop Hollow, Columbus, OH", "2525 Ashfield Estate, Tampa, FL", "2626 Redwoodvale Road, Memphis, TN", "2727 Sycamorecrest Lane, Chicago, IL", "2828 Dogwoodspirit Place, Albuquerque, NM", "2929 Chestnutfort Drive, Omaha, NE", "3030 Alderwood Quay, St. Louis, MO", "3131 Cottonwoodtrace Court, San Francisco, CA", "3232 Magnoliawood Knoll, Jacksonville, FL", "3333 Maplebranch View, Louisville, KY", "3434 Birchcrest Bend, Philadelphia, PA", "3535 Cypresswave Terrace, Detroit, MI", "3636 Beechwoodcove Point, Cleveland, OH", "3737 Elmcrest Passage, El Paso, TX", "3838 Spruceglade Circle, Denver, CO", "3939 Willowfield Rise, Austin, TX", "4040 Hickoryview Hill, Seattle, WA"]

        patient_notes = ["Patient reports mild chest discomfort lasting 15 minutes after exercise.", "No fever or chills, but patient complains of fatigue over the past week.", "Noted slight swelling in the right ankle, likely due to sprain.", "Blood pressure elevated at 145/90; recommend lifestyle adjustments.", "Patient denies any allergies but mentions sensitivity to strong odors.", "Follow-up required for persistent headaches despite current medication.", "Cough persists for two weeks; order chest X-ray to rule out infection.", "Patient is experiencing occasional dizziness when standing up quickly.", "Skin rash noted on left arm, no itching reported.", "Lab results show elevated cholesterol; dietary changes discussed.", "Complains of difficulty sleeping, potentially linked to increased stress.", "Reports recent onset of joint pain in fingers, likely mild arthritis.", "Seasonal allergies worsening; prescribed antihistamines.", "Weight loss of 5 lbs noted since last visit; patient denies intentional dieting.", "Reports nausea and occasional vomiting after meals; order ultrasound.", "No significant changes in diabetes management; continue current plan.", "Patient experiences shortness of breath while climbing stairs.", "Ear pain persists despite initial treatment; prescribed stronger antibiotics.", "Mild fever of 100.2°F reported over the last two days.", "Complains of tingling sensation in right hand; schedule nerve conduction test.", "Reports blurry vision in the evenings; refer to ophthalmologist.", "Mole on upper back appears irregular; biopsy recommended.", "Notes improved mobility following physical therapy for knee injury.", "Patient reports increased thirst and frequent urination; check glucose levels.", "Complains of mild abdominal discomfort after eating spicy food.", "No new symptoms reported; medication refills provided.", "Experiencing intermittent chest tightness; scheduled stress test.", "Patient reports difficulty hearing in left ear; schedule audiogram.", "Frequent heartburn persists; consider endoscopy.", "Patient mentions occasional palpitations; recommend Holter monitor.", "Reports persistent fatigue despite adequate sleep; screen for anemia.", "Minor bruising on left forearm; no history of trauma reported.", "Complains of tension headaches, possibly linked to screen time.", "Blood sugar levels stable; no adjustment to insulin required.", "Experiencing back pain after heavy lifting; recommend physiotherapy.", "Patient denies any recent illness but reports increased hair loss.", "No significant side effects reported from new medication.", "Reports sore throat and swollen glands; rapid strep test ordered.", "Follow-up needed for elevated liver enzymes from last blood test.", "Complains of dry, itchy skin; prescribed hydrating ointment.", "Patient denies smoking but reports occasional vaping.", "Mild swelling in both feet noted; recommend compression stockings.", "Reports difficulty concentrating; assess for potential ADHD.", "X-ray confirms minor fracture in left wrist; splint applied.", "Patient feels generally well but requests flu vaccination.", "Experiencing occasional nosebleeds; check coagulation profile.", "Notes improved sleep after starting melatonin supplement.", "Patient reports increased anxiety; consider therapy referral.", "Mild fever subsided; no further intervention required.", "Complains of loss of appetite; screen for underlying causes."]

        for i in range(50): #add all 50 patients
            self.controller.create_patient(phns_list[i], names_list[i], birthdays_list[i], phone_numbers_list[i], emails_list[i], adresses_list[i])
            self.controller.set_current_patient(phns_list[i])
            for x in range(10): #add 10 random notes from the list
                random_number = random.randint(0, 49)
                self.controller.create_note(patient_notes[random_number])

def main():
    user_input = None

    while True:
        try:
            user_input = int(input("Enter 1 to populate files, 0 to just clear, or 3 to exit: "))
            if user_input == 3:
                sys.exit(1)
            if user_input != 1 and user_input !=0:
                raise ValueError
            break
        except ValueError as e:
            print("invalid input:")
            print("     -enter 0 to clear files")
            print("     -or 1 to clear and populate files")

    if user_input==1:
        resetAndAddContent(True)
        print("files reset and populated")
    else:
        resetAndAddContent(False)
        print("files reset")

if __name__ == '__main__':
    main()