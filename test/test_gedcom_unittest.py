import unittest
import development.ACHUAH_gedcom_parser
import datetime
from datetime import date
from development.ACHUAH_gedcom_parser import individuals, familyTable

table = development.ACHUAH_gedcom_parser.createTables("../development/ACHUAH_FAMILY.GED")
month_dict = {"JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12}

class TestGEDCOM(unittest.TestCase):
    # US01 - Dates before the current date
    def dates_before_currDate(self):
        for family in table[1]:
                for indiv in table[0]:
                    if (indiv.id == family.husband or indiv.id == family.wife):
                        # print(family.married)
                        temp_married = family.married.split(" ")
                        temp_birth = indiv.birth.split(" ")
                        checkDate = (datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0])))
                        if(not checkDate):
                            print('Dates (birth, marriage, divorce, death) should not be after the current date')
                            break
        print("Here")
        self.assertNotEqual(checkDate, False)

    # US02 - Birth before marriage
    def birth_before_marr(self):
        return

    # US03 - Birth before death
    def birth_before_death(self):
        return

    # US04
    def marr_before_div(self):
        return
    
    # US05
    def us05(self):
        return

    # US6
    def us06(self):
        return

if __name__ == '__main__':
    unittest.main()