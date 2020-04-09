import os
import extract_text
import extract_fields
import unittest

class test_criminal_complaints(unittest.TestCase):
    doc = open(os.path.expanduser(_______________)).read()
     answers = extract_fields.probation_form(doc)

    def test_PCF(self):
        input = self.answers['PCF']
        expected = 'TEST'
        self.assertEqual(input, expected)
    
    def test_DOB(self):
        input = self.answers['DOB']
        expected = 'TEST'
        self.assertEqual(input, expected)

    def test_age(self):
        input = self.answers['Age']
        expected = 'TEST'
        self.assertEqual(input, expected)
    
    def test_birthplace(self):
        input = self.answers['Birthplace']
        expected = 'TEST'
        self.assertEqual(input, expected)
    

    def test_mother(self):
        input = self.answers['Mother']
        expected = ''
        self.assertEqual(input, expected)
    
    def test_father(self):
        input = self.answers['Father']
        expected = ''
        self.assertEqual(input, expected)
    
    def test_height(self):
        input = self.answers['Height']
        expected = ''
        self.assertEqual(input, expected)

    def test_weight(self):
        input = self.answers['Weight']
        expected = ''
        self.assertEqual(input, expected)
    
    def test_hair(self):
        input = self.answers['Hair']
        expected = 'Black'
        self.assertEqual(input, expected)
    
    def test_eyes(self):
        input = self.answers['Eyes']
        expected = 'Brown'
        self.assertEqual(input, expected)

    def test_gender(self):
        input = self.answers['Gender']
        expected = 'M'
        self.assertEqual(input, expected)
    

    def test_race(self):
        input = self.answers['Race']
        expected = 'Black/ African America'
        self.assertEqual(input, expected)
    
    def test_ethnicity(self):
        input = self.answers['Ethnicity']
        expected = 'None Hispanic or Latino'
        self.assertEqual(input, expected)
    
    def test_dln(self):
        input = self.answers['DLN']
        expected = 'NONE'
        self.assertEqual(input, expected)
    
    def test_cari(self):
        input = self.answers['CARI']
        expected = 'TEST'
        self.assertEqual(input, expected)
    
    def test_records_include(self):
        input = self.answers['Records Include']
        expected = 'Test'
        self.assertEqual(input,expected)

if __name__ == "__main__":
    unittest.main()
    
    