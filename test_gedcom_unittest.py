import unittest
import ACHUAH_gedcom_parser
import datetime
from datetime import date
from ACHUAH_gedcom_parser import individuals, familyTable

table = ACHUAH_gedcom_parser.createTables("ACHUAH_FAMILY.GED")
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

# print(table[0][0].id)
# print(table[1][0].husb_id)

class TestGEDCOM(unittest.TestCase):
    # US01 - Dates before the current date
    def test_dates_before_currDate(self):
        today = datetime.datetime.today()

        for person in table[0]:
            self.assertNotEqual(person.birthday, None, "Error: birthday cannot be None")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
            self.assertLess(birthday, today, "Error: birthday cannot be before today")

            if person.death != "N/A":
                deathDaySplit = person.death.split(" ")
                deathDay = datetime.datetime(int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))
                self.assertLess(deathDay, today, "Error: deathday cannot be before today")

        for family in table[1]:
            for individual in table[0]:
                if(individual.id == family.husb_id or individual.id == family.wife_id):
                    if family.married != "N/A":
                        marriedSplit = family.married.split(" ")
                        marriedDay = datetime.datetime(int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))
                        self.assertLess(marriedDay, today, "Error: married day cannot be before today")
                    if(family.divorced != "N/A"):
                        divorcedSplit = family.divorced.split(" ")
                        divorcedDay = datetime.datetime(int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))
                        self.assertLess(divorcedDay, today, "Error: divorced day cannot be before today")


    # # US02 - Birth before marriage
    def test_birth_before_marr(self):
        for person in table[0]:
            self.assertNotEqual(person.birthday, None, "Error: birthday cannot be None")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
        for family in table[1]:
            for individual in table[0]:
                if(individual.id == family.husb_id or individual.id == family.wife_id):
                    if family.married != "N/A":
                        marriedSplit = family.married.split(" ")
                        marriedDay = datetime.datetime(int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

        self.assertLess(birthday, marriedDay, "Error: birthday must be before the married day")

    # US03 - Birth before death
    def test_birth_before_death(self):
        for person in table[0]:
            self.assertNotEqual(person.birthday, None, "Error: birthday cannot be None")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))    


            if(person.death == "N/A"):
                print("Person has not died yet")
                continue
            deathDaySplit = person.death.split(" ")
            deathDay = datetime.datetime(int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))        
            self.assertLess(birthday, deathDay, "Error: person cannot die before their birthday")
    # # US04 - Marriage before divorce
    # def test_marr_before_div(self):
    #     return
    
    # # US05 - Marriage before death
    # def test_marr_before_death(self):
    #     return

    # # US06 - Divorce before death
    # def test_div_before_death(self):
    #     return

if __name__ == '__main__':
    unittest.main()