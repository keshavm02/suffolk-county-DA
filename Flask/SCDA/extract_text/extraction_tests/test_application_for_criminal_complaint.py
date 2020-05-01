import sys
sys.path.append('..')
import unittest
import os
import extract_fields


class test_application_for_criminal_complaint(unittest.TestCase):
    doc = open(os.path.abspath("test_textdumps/Application for Criminal Complaint .txt")).read()
    answers = extract_fields.extract_application_for_criminal_complaint(doc)

    def test_summons(self):
        input = self.answers["Summons"]
        expected = "No"
        self.assertEqual(input, expected)


    def test_hearing_requested(self):
        input = self.answers["Hearing Requested"]
        expected = "No"
        self.assertEqual(input, expected)


    def test_Court(self):
        input = self.answers["Court"]
        expected = "001 - BOSTON MUNICIPAL COURT"
        self.assertEqual(input, expected)


    def test_arrest_status_of_accused(self):
        input = self.answers["Arrest Status of Accused"]
        expected = "Has been arrested"
        self.assertEqual(input, expected)


    def test_arrest_date(self):
        input = self.answers["Arrest Date"]
        expected = "09/02/2017"
        self.assertEqual(input, expected)


    def test_in_custody(self):
        input = self.answers["In Custody"]
        expected = "Yes"
        self.assertEqual(input, expected)



    def test_officer_id(self):
        input = self.answers["Officer ID No."]
        expected = "144484"
        self.assertEqual(input, expected)

    #Need to fix this
    def test_agency(self):
        input = self.answers["Agency"]
        expected = "654- BOSTON PD - AREA B-3"
        self.assertEqual(input, expected)


    def test_type(self):
        input = self.answers["Type"]
        expected = "Person"
        self.assertEqual(input, expected)


    def test_name(self):
        input = self.answers["Name"]
        expected = "Iouis, Bepie Jalani"
        self.assertEqual(input, expected)


    def test_birth_surname(self):
        input = self.answers["Birth Surname"]
        expected = ""
        self.assertEqual(input, expected)


    def test_address(self):
        input = self.answers["Address"]
        expected = "28 Abbot St, Dorchester, MA 02124"
        self.assertEqual(input, expected)


    def test_dob(self):
        input = self.answers["Date of Birth"]
        expected = "02/10/1981"
        self.assertEqual(input, expected)


    def test_place_of_birth(self):
        input = self.answers["Place of Birth"]
        expected = "MA - MASSACHUSETTS"
        self.assertEqual(input, expected)


    def test_ssn(self):
        input = self.answers["Social Security No."]
        expected = "025-80-0033"
        self.assertEqual(input, expected)


    def test_pcf_number(self):
        input = self.answers["PCF No."]
        expected = ""
        self.assertEqual(input, expected)


    def test_sid(self):
        input = self.answers["SID"]
        expected = ""
        self.assertEqual(input, expected)


    def test_marital_status(self):
        input = self.answers["Marital Status"]
        expected = "S-Single"
        self.assertEqual(input, expected)


    def test_drivers_license_number(self):
        input = self.answers["Driver's License No."]
        expected = "S94459452"
        self.assertEqual(input, expected)


    def test_drivers_license_state(self):
        input = self.answers["Driver's License State"]
        expected = "MA- Massachusetts"
        self.assertEqual(input, expected)


    def test_drivers_license_exp(self):
        input = self.answers["Driver's License Exp. Year"]
        expected = ""
        self.assertEqual(input, expected)


    def test_gender(self):
        input = self.answers["Gender"]
        expected = "M- MALE"
        self.assertEqual(input, expected)


    def test_race(self):
        input = self.answers["Race"]
        expected = "-"
        self.assertEqual(input, expected)


    def test_height(self):
        input = self.answers["Height"]
        expected = "5'11\""
        self.assertEqual(input, expected)


    def test_weight(self):
        input = self.answers["Weight"]
        expected = "180 lbs"
        self.assertEqual(input, expected)


    def test_eyes(self):
        input = self.answers["Eyes"]
        expected = "BRO- BROWN"
        self.assertEqual(input, expected)


    def test_hair(self):
        input = self.answers["Hair"]
        expected = "BLK - Black"
        self.assertEqual(input, expected)


    def test_ethnicity(self):
        input = self.answers["Ethnicity"]
        expected = "N - non Hispanic"
        self.assertEqual(input, expected)


    def test_primary_language(self):
        input = self.answers["Primary Language"]
        expected = "eng- English"
        self.assertEqual(input, expected)


    def test_complexion(self):
        input = self.answers["Complexion"]
        expected = "MBR - MEDIUM BROWN"
        self.assertEqual(input, expected)


    def test_scars_marks_tattoos(self):
        input = self.answers["Scars/Marks/Tattoos"]
        expected = "DOT ART ARM - Arm, nonspecific, artifical(tatoos)"
        self.assertEqual(input, expected)


    def test_employer_name(self):
        input = self.answers["Employer Name"]
        expected = ""
        self.assertEqual(input, expected)


    def test_school_name(self):
        input = self.answers["School Name"]
        expected = ""
        self.assertEqual(input, expected)


    def test_day_phone(self):
        input = self.answers["Day Phone"]
        expected = "(857) 272-8678"
        self.assertEqual(input, expected)


    def test_mother_name(self):
        input = self.answers["Mother Name"]
        expected = "Louis, Emeriane"
        self.assertEqual(input, expected)


    def test_mother_maiden_name(self):
        input = self.answers["Mother Maiden Name"]
        expected = ""
        self.assertEqual(input, expected)


    def test_father_name(self):
        input = self.answers["Father Name"]
        expected = "Louis, Yvonne"
        self.assertEqual(input, expected)


    def test_complainant_type(self):
        input = self.answers["Complainant Type"]
        expected = "Police"
        self.assertEqual(input, expected)


    def test_police_department(self):
        input = self.answers["Police Dept."]
        expected = "BOSTON POLICE DEPARTMENT"
        self.assertEqual(input, expected)


if __name__ == "__main__":
    unittest.main()