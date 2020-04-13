import os
import extract_text
import extract_fields
import unittest

class test_criminal_complaints(unittest.TestCase):
    doc = open(os.path.expanduser("~/suffolk-county-DA/extract_text/extraction_tests/test_textdumps/Incident Report Dump.txt")).read()

    def test_case_number(self):
        input = extract_fields.find_case_number(self.doc)
        expected = 'I172072717'
        self.assertEqual(input, expected)

    def test_cad_incident_number(self):
        input = extract_fields.find_cad_incident_number(self.doc)
        expected = 'P170462082'
        self.assertEqual(input, expected)


    def test_report_type(self):
        input = extract_fields.find_report_type(self.doc)
        expected = 'Incident Report'
        self.assertEqual(input, expected)

    def test_date_time_occurred(self):
        input = extract_fields.find_date_time(self.doc)[0]
        expected = '09/02/2017 09:14'
        self.assertEqual(input, expected)

    def test_date_time_reported(self):
        input = extract_fields.find_date_time(self.doc)[1]
        expected = '09/02/2017 09:14'
        self.assertEqual(input, expected)

    def test_public_narrative(self):
        input = extract_fields.find_public_narrative(self.doc)
        expected = "TEST"
        self.assertEqual(input, expected)





if __name__ == "__main__":
    unittest.main()