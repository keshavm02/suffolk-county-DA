import sys
sys.path.append('..')
import unittest
import os
import extract_fields

class test_arrest_booking_form(unittest.TestCase):
    doc = open(os.path.expanduser("~/suffolk-county-DA/Flask/SCDA/extract_text/extraction_tests/test_textdumps/Arrest Booking Form Dump.txt")).read()
    answers = extract_fields.extract_arrest_booking_form(doc)

    def test_report_date(self):
        input = self.answers['Report Date']
        #print(report_date_input)
        expected = '10/24/2019 11:47'
        self.assertEqual(input, expected)

    def test_booking_status(self):
        input = self.answers['Booking Status']
        expected = 'Verified'
        self.assertEqual(input, expected)

    def test_printed_by(self):
        input = self.answers['Printed By']
        expected = 'PINKHAM, Deirdre'
        self.assertEqual(input, expected)

    def test_district(self):
        input = self.answers['District']
        expected = '04'
        self.assertEqual(input, expected)

    def test_ucr_code(self):
        input = self.answers['UCR Code']
        expected = '0803'
        self.assertEqual(input, expected)

    def test_OBTN(self):
        input = self.answers['OBTN']
        expected = 'TBOS190035706'
        self.assertEqual(input, expected)

    def test_court_of_appearance(self):
        input = self.answers['Court of Appearance']
        expected = 'Boston Municipal Court'
        self.assertEqual(input, expected)

    def test_master_name(self):
        input = self.answers['Master Name']
        expected = 'GRIFFITH, Tianna Celina'
        self.assertEqual(input, expected)

    def test_age(self):
        input = self.answers['Age']
        expected = '18'
        self.assertEqual(input, expected)

    def test_location_of_arrest(self):
        input = self.answers['Location of Arrest']
        expected = '90 Warren Ave, Boston'
        self.assertEqual(input, expected)

    def test_booking_name(self):
        input = self.answers['Booking Name']
        expected = 'GRIFFITH, Tianna Celina'
        self.assertEqual(input, expected)

    def test_alias(self):
        input = self.answers['Alias']
        expected = ''
        self.assertEqual(input, expected)

    #Not working, need to fix
    def test_address(self):
        input = self.answers['Personal Address']
        expected = '2 Savin Street, ROXBURY MA 02119 US'
        #print(input)
        self.assertEqual(input, expected)

    def test_charges(self):
        input = self.answers['Charges']
        expected = 'Assault and Battery on a Police Officer (No injuries) (265-13D)'
        self.assertEqual(input, expected)

    def test_booking_no(self):
        input = self.answers['Booking #']
        expected = '19-00357-06'
        self.assertEqual(input, expected)

    def test_incident_no(self):
        input = self.answers['Incident #']
        expected = '192086122'
        self.assertEqual(input, expected)

    def test_CR_number(self):
        input = self.answers['CR Number']
        expected = '502528-19'
        self.assertEqual(input, expected)

    def test_booking_date(self):
        input = self.answers['Booking Date']
        expected = '10/24/2019 09:15'
        self.assertEqual(input, expected)

    def test_arrest_date(self):
        input = self.answers['Arrest Date']
        expected = '10/24/2019 09:00'
        self.assertEqual(input, expected)

    def test_RA_number(self):
        input = self.answers['RA Number']
        expected = ''
        self.assertEqual(input, expected)

    def test_sex(self):
        input = self.answers['Sex']
        expected = 'Female'
        self.assertEqual(input, expected)

    def test_height(self):
        input = self.answers['Height']
        expected = '5\'07'
        self.assertEqual(input, expected)

    def test_occupation(self):
        input = self.answers['Occupation']
        expected = 'Student'
        self.assertEqual(input, expected)

    def test_race(self):
        input = self.answers['Race']
        expected = 'Black Non-Hispanic'
        self.assertEqual(input, expected)

    def test_weight(self):
        input = self.answers['Weight']
        expected = '160 lbs'
        self.assertEqual(input, expected)

    def test_employer(self):
        input = self.answers['Employer/School']
        expected = 'Mckinley'
        self.assertEqual(input, expected)

    def test_DOB(self):
        input = self.answers['Date of Birth']
        expected = '05/09/2001'
        self.assertEqual(input, expected)

    def test_build(self):
        input = self.answers['Build']
        expected = 'Medium'
        self.assertEqual(input, expected)

    def test_emp_address(self):
        input = self.answers['Emp/School Addr']
        expected = 'MA US'
        self.assertEqual(input, expected)

    def test_POB(self):
        input = self.answers['Place of Birth']
        expected = 'ST PETER BB'
        self.assertEqual(input, expected)

    def test_eye_color(self):
        input = self.answers['Eyes Color']
        expected = 'Brown'
        self.assertEqual(input, expected)

    def test_social_sec_no(self):
        input = self.answers['Social Sec. Number']
        expected = ''
        self.assertEqual(input, expected)

    def test_marital_status(self):
        input = self.answers['Marital Status']
        expected = 'Single'
        self.assertEqual(input, expected)

    def test_hair_color(self):
        input = self.answers['Hair Color']
        expected = 'Black'
        self.assertEqual(input, expected)

    def test_operators_license(self):
        input = self.answers['Operators License']
        expected = ''
        self.assertEqual(input, expected)

    def test_mothers_name(self):
        input = self.answers['Mother\'s Name']
        expected = 'GRIFFITH, Collene'
        self.assertEqual(input, expected)

    def test_complexion(self):
        input = self.answers['Complexion']
        expected = ''
        self.assertEqual(input, expected)

    def test_state(self):
        input = self.answers['State']
        expected = 'MA'
        self.assertEqual(input, expected)

    def test_fathers_name(self):
        input = self.answers['Father\'s Name']
        expected = 'BRADFORD, Andrew'
        self.assertEqual(input, expected)

    def test_phone_used(self):
        input = self.answers['Phone Used']
        expected = 'Yes'
        self.assertEqual(input, expected)

    def test_scars(self):
        input = self.answers['Scars/Marks/Tattoos']
        expected = ''
        self.assertEqual(input, expected)

    def test_hospital(self):
        input = self.answers['Examined at Hospital']
        expected = 'No'
        self.assertEqual(input, expected)

    def test_clothing(self):
        input = self.answers['Clothing Desc']
        expected = 'green jacket, grey sweatshirt, black pants, black sneakers'
        self.assertEqual(input, expected)

    def test_breathalyzer(self):
        input = self.answers['Breathalyzer Used']
        expected = 'No'
        self.assertEqual(input, expected)

    def test_EMS(self):
        input = self.answers['Examined by EMS']
        expected = 'No'
        self.assertEqual(input, expected)

    def test_arresting_officer(self):
        input = self.answers['Arresting Officer']
        expected = 'BSP 06057 STEVENS, Ames'
        self.assertEqual(input, expected)

    def test_cell_no(self):
        input = self.answers['Cell Number']
        expected = ''
        self.assertEqual(input, expected)

    def test_booking_officer(self):
        input = self.answers['Booking Officer']
        expected = 'BPD 102191 BANKS, Madeline'
        self.assertEqual(input, expected)

    def test_partner(self):
        input = self.answers['Partner\'s #']
        expected = ''
        self.assertEqual(input, expected)

    def test_rights(self):
        input = self.answers['Informed of Rights']
        expected = 'BPD 120909 MURPHY, Colleen'
        self.assertEqual(input, expected)

    def test_unit(self):
        input = self.answers['Unit #']
        expected = 'TZ236'
        self.assertEqual(input, expected)

    def test_cell_placer(self):
        input = self.answers['Placed in Cell By']
        expected = 'BPD 102191 BANKS, Madeline'
        self.assertEqual(input, expected)

    def test_trans_unit(self):
        input = self.answers['Trans Unit #']
        expected = 'D441D'
        self.assertEqual(input, expected)

    def test_searcher(self):
        input = self.answers['Searched By']
        expected = 'BPD 102191 BANKS, Madeline'
        self.assertEqual(input, expected)

    def test_cautions(self):
        input = self.answers['Cautions']
        expected = ''
        self.assertEqual(input, expected)

    #Not working, ask Nasser about format
    def test_booking_comments(self):
        input = self.answers['Booking Comments']
        expected = 'bop and q5 completed'
        self.assertEqual(input, expected)

    #Not working, ask Nasser about format
    def test_injuries(self):
        input = self.answers['Visible Injuries']
        expected = 'none'
        self.assertEqual(input, expected)

    def test_person_notified(self):
        input = self.answers['Person Notified']
        expected = ''
        self.assertEqual(input, expected)

    def test_relationship(self):
        input = self.answers['Relationship']
        expected = ''
        self.assertEqual(input, expected)

    def test_phone(self):
        input = self.answers['Phone']
        expected = ''
        self.assertEqual(input, expected)

    def test_juv_address(self):
        input = self.answers['Address']
        #print(input)
        expected = ''
        self.assertEqual(input, expected)

    def test_jov_prob_off(self):
        input = self.answers['Juv. Prob. Officer']

        expected = ''
        self.assertEqual(input, expected)

    def test_notifier(self):
        input = self.answers['Notified By']
        expected = ''
        self.assertEqual(input, expected)

    def test_notify_date(self):
        input = self.answers['Notified Date/Time']
        expected = ''
        self.assertEqual(input, expected)

    def test_bail_setter(self):
        input = self.answers['Bail Set By']
        expected = ''
        self.assertEqual(input, expected)

    def test_select(self):
        input = self.answers['I Selected the Bail Comm.']
        expected = ''
        self.assertEqual(input, expected)

    def test_bailer(self):
        input = self.answers['Bailed By']
        expected = ''
        self.assertEqual(input, expected)

    def test_amount(self):
        input = self.answers['Amount']
        expected = ''
        self.assertEqual(input, expected)

    def test_bop_check(self):
        input = self.answers['BOP Check']
        expected = 'BPD 120909 MURPHY, Colleen'
        self.assertEqual(input, expected)

    def test_suicide(self):
        input = self.answers['Suicide Check']
        expected = ''
        self.assertEqual(input, expected)

    def test_bop_warrant(self):
        input = self.answers['BOP Warrant']
        expected = ''
        self.assertEqual(input, expected)

    def test_bop_court(self):
        input = self.answers['BOP Court']
        expected = ''
        self.assertEqual(input, expected)



if __name__ == "__main__":
    unittest.main()