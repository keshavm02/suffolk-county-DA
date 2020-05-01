import sys
sys.path.append('.././suffolk-county-DA/Flask/SCDA/')
import unittest
import os
from extract_text import extract_fields

class test_miranda(unittest.TestCase):
    doc = open(os.path.expanduser("~/suffolk-county-DA/Flask/SCDA/extract_text/extraction_tests/test_textdumps/Miranda Text Dump.txt")).read()
    answers = extract_fields.extract_miranda_form(doc)

    def test_booking_name(self):
        input = self.answers['Booking Name']
        expected = 'OJO'
        self.assertEqual(input, expected)
    def test_first_name(self):
        input = self.answers['First']
        expected = 'David'
        self.assertEqual(input, expected)
    def test_middle_name(self):
        input = self.answers['Middle']
        expected = 'O'
        self.assertEqual(input, expected)
    def test_suffix(self):
        input = self.answers['Suffix']
        expected = ''
        self.assertEqual(input, expected)
    def test_home_address(self):
        input = self.answers['Home Address']
        expected = '60 Bridal Path CR #728, RANDOLPH MA US'
        self.assertEqual(input, expected)
    def test_report_date(self):
        input = self.answers['Report Date']
        expected = '05/05/2015 14:50'
        self.assertEqual(input, expected)
    def test_booking_status(self):
        input = self.answers['Booking Status']
        expected = 'Unverified'
        self.assertEqual(input, expected)
    def test_printed_by(self):
        input = self.answers['Printed By']
        expected = 'THOMAS, Joslin A'
        self.assertEqual(input, expected)
    def test_sex(self):
        input = self.answers['Sex']
        expected = 'Male'
        self.assertEqual(input, expected)
    def test_race(self):
        input = self.answers['Race']
        expected = 'Black Hispanic'
        self.assertEqual(input, expected)
    def test_dob(self):
        input = self.answers['Date of Birth']
        expected = '04/04/1970'
        self.assertEqual(input, expected)
    def test_district(self):
        input = self.answers['District']
        expected = '11'
        self.assertEqual(input, expected)
    def test_booking_number(self):
        input = self.answers['Booking Number']
        expected = '15-00628-11'
        self.assertEqual(input, expected)
    def test_arrest_date(self):
        input = self.answers['Arrest Date']
        expected = '05/05/2015 13:30'
        self.assertEqual(input, expected)
    def test_incident_number(self):
        input = self.answers['Incident Number']
        expected = '15203897'
        self.assertEqual(input, expected)
    def test_booking_date(self):
        input = self.answers['Booking Date']
        expected = '05/05/2015 14:30'
        self.assertEqual(input, expected)
    def test_charges(self):
        input = self.answers['Charges']
        expected = 'Rape and Abuse of A Child Under 16 (265:23) (Docket #:1507CR001640);Dorchester distr'
        self.assertEqual(input, expected)
    def test_telephone_used(self):
        input = self.answers['Telephone Used']
        expected = 'Yes'
        self.assertEqual(input, expected)
    def test_breathalyzer_used(self):
        input = self.answers['Breathalyzer Used']
        expected = 'No'
        self.assertEqual(input, expected)
    def test_examined_at_hospital(self):
        input = self.answers['Examined at Hospital']
        expected = 'No'
        self.assertEqual(input, expected)
    def test_examined_by_ems(self):
        input = self.answers['Examined by EMS']
        expected = 'No'
        self.assertEqual(input, expected)
    def test_visible_injuries(self):
        input = self.answers['Visible Injuries']
        expected = 'none'
        self.assertEqual(input, expected)
    def test_money(self):
        input = self.answers['Money']
        expected = '2.10'
        self.assertEqual(input, expected)
    def test_storage_no(self):
        input = self.answers['Property Storage No']
        expected = ''
        self.assertEqual(input, expected)
    def test_property(self):
        input = self.answers['Property']
        expected = 'brown belt, two wrist bands, set of keys'
        self.assertEqual(input, expected)

if __name__ == '__main__':
    unittest.main()
