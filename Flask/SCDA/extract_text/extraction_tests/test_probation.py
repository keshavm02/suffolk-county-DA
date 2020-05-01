import sys
sys.path.append('..')
import unittest
import os
import extract_fields


class test_criminal_complaints(unittest.TestCase):
    doc = open(os.path.abspath('test_textdumps/Probation Textdump.txt')).read()
    answers = extract_fields.extract_probation_form(doc)


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
        expected = 'TEST'
        self.assertEqual(input, expected)


    def test_father(self):
        input = self.answers['Father']
        expected = 'TEST'
        self.assertEqual(input, expected)


    def test_height(self):
        input = self.answers['Height']
        expected = 'TEST'
        self.assertEqual(input, expected)


    def test_weight(self):
        input = self.answers['Weight']
        expected = 'TEST'
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
        expected = 'Black / African American'
        self.assertEqual(input, expected)


    def test_ethnicity(self):
        input = self.answers['Ethnicity']
        expected = 'Non Hispanic or Latino'
        self.assertEqual(input, expected)


    def test_dln(self):
        input = self.answers['DLN']
        expected = 'NONE'
        self.assertEqual(input, expected)


    def test_cari(self):
        input = self.answers['CARI']
        expected = str(['CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'POSS FIREARM W/O PERMIT (FIR POSS WO PERM)DISPOSITION: C [Redacted]G 3-4YR '
 'CMTD CONCSTATUS: CLOSED',
 'CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'ASSAULT DANGEROUS WEAPON (ASLT DW)DISPOSITION: C [Redacted] G 3-3YR 1DA CMTD '
 'CONCSTATUS: CLOSED',
 'CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'ASSAULT DANGEROUS WEAPON (ASLT DW)DISPOSITION: C [Redacted] G 3-4YR CMTD '
 'CONCSTATUS: CLOSED',
 'CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'ASSAULT DANGEROUS WEAPON (ASLT DW)DISPOSITION: C [Redacted] G PROB 3YR F&A '
 'CONCSTATUS: OPEN',
 'CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'ASSAULT DANGEROUS WEAPON (ASLT DW)DISPOSITION: C [Redacted] G PROB 3YR F&A '
 'CONCSTATUS: OPEN',
 'CA DKT#: TESTDT: TEST Boston PD - 754 CRT: SUFFOLK SUPERIOR (84)OFFENSE: '
 'CARRY FIR W/ AMMUNITION (FIR CARRY W/AMM)DISPOSITION: C [Redacted] G PROB '
 '3YR F&A CONCSTATUS: OPEN',
 'CA DKT#: TESTDT: TEST Suffolk County Sheriff CRT: BOSTON BMC CENTRAL '
 'DISTRICT (1)'])
        self.assertEqual(input, expected)


    def test_records_include(self):
        input = self.answers['Records Include']
        #print(input)
        expected = 'PCF = TEST Case Number = , Docket Report Group = ALL,' + '\n' + 'Docket Code = ALL, Include Linked Charges = False, Include Linked Cases = True'
        #print(expected)
        self.assertEqual(input, expected)


if __name__ == "__main__":
    unittest.main()
