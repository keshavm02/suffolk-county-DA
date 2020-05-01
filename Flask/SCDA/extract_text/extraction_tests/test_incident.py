import sys
sys.path.append('.././suffolk-county-DA/Flask/SCDA/')
import unittest
import os
from extract_text import extract_fields

class test_incident_report(unittest.TestCase):
    doc = open(os.path.expanduser("~/suffolk-county-DA/Flask/SCDA/extract_text/extraction_tests/test_textdumps/Incident Report Dump.txt")).read()

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
        expected = """About 9:14 AM on Saturday 9/2/17 Officer Palermo in the C431D observed a motor vehicle fail to stop at a stop sign on the corner of Old Rd.
and Columbia Rd. Dorchester.

Officer Palermo activated her emergency lights and sirens and pulled over the Red 2003 Saturn LW300 with MA plates 3ZD537 at the intersection of Columbia Rd and Seaver St. Officer Palermo noted that the vehicle was occupied one time. Prior to exiting the department vehicle Officer Palermo ran the vehicles license plate through CJIS. The CJIS search of MA 3ZD537 resulted in an expired/non-renewed registration of a white 2008 Infinity G37 that's registration expired on July 31, 2017.

Officer Palermo approached the vehicle on the drivers side and asked the operator BEPIE JALANI LOUIS for his license and registration. The
driver told Officer Palermo that he had a really stressful morning and had been kicked out of his home, and was moving his belongings to his
new address at 28 Abbot St. Dorchester. The driver was asked again for his license and registration, at which time he retrieved his drivers license
from his right rear pants pocket, handed it to the Officer and told her that he had just purchased the vehicle. Officer Palermo asked if he had any
proof of purchase or registry documents. Mr. Louise provided expired registration with someone elses name on it and a title to the vehicle also
with someone elses name on it. There was also a dealership warentee aggreement dated 8/10/17 with an illegible signature and no name of
purchaser stated on the document.

Officer Palermo ran the operators drivers license number through CJIS which showed a revoked license. The CJIS results also showed a charge on
6/7/17 less than two months prior of operating after a suspended license and repeated charges for the same and obstructed/failure to display
paltes violations dating back 8 years. Officer Palermo called for an assisting unit. The C425D (Gomes) came to the scene. Officers approached
the vehicle and the driver was told that his license was revoked and the driver asked "do I have to step out of the vehicle?" Officers answered yes. The driver stepped out of the vehicle and was instructed by Officer Palermo to turn around and place his hands behind his back. The driver
was handcuffed and placed in the rear of the C425D department vehicle.

Officer Palermo ran the vehicles VIN through CJIS which showed that the vehicle was unregistered and uninsured. Officer Palermo called for a
motor vehicle tow to the scene. MJS Towing came and towed the vehicle (Slip #3687). An inventory log was filled out by Officer Palermo and the tow log was filled in. Tow line notified (Boudreau). The Motor vehicle plates were removed fromthe vehicle and turned into the B-3 Auto
Investigator.

The driver, BEPIE JALANI LOUIS, was arrested for:

OPERATING A MOTOR VEHICLE AFTER REVOCATION OF LICENSE ch: 90 sec. 23
OPERATING A MOTOR VEHICLE AFTER REVOCATION OF REGISTRATION ch: 90 sec. 23
OPERATING A MOTOR VEHICLE WITHOUT INSURANCE ch: 90 sec. 34j

ATTACHING PLATES VIOLATION ch: 90 sec. 23

    
     
 

In addition the driver was issued a citation for failure to stop for a stop sign (R8623526)

The suspect was transfered to B-3 by the C425D (Gomes) and booked (Banks)."""
        self.assertEqual(input, expected)





if __name__ == "__main__":
    unittest.main()