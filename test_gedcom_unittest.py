import unittest
import ACHUAH_gedcom_parser
import datetime

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

class TestGEDCOM(unittest.TestCase):
    # US01 - Dates before the current date
    def test_dates_before_currDate(self):
        today = datetime.datetime.today()

        for person in table[0]:
            self.assertNotEqual(person.birthday, None, "Error: Birthday cannot be None")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
            self.assertLess(birthday, today, "Error: Birthday cannot be before today")

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
                        self.assertLess(marriedDay, today, "Error: Married day cannot be before today")
                    if family.divorced != "N/A":
                        divorcedSplit = family.divorced.split(" ")
                        divorcedDay = datetime.datetime(int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))
                        self.assertLess(divorcedDay, today, "Error: Divorced day cannot be before today")

    # # US02 - Birth before marriage
    def test_birth_before_marr(self):
        for family in table[1]:
            for individual in table[0]:
                if individual.id == family.husb_id or individual.id == family.wife_id:
                    if family.married != "N/A":
                        marriedSplit = family.married.split(" ")
                        marriedDay = datetime.datetime(int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                        self.assertNotEqual(individual.birthday, None, "Error: Birthday cannot be None")
                        birthDaySplit = individual.birthday.split(" ")
                        birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))

                    self.assertLess(birthday, marriedDay, "Error: Birthday must be before the married day!")

    # US03 - Birth before death
    def test_birth_before_death(self):
        for person in table[0]:
            self.assertNotEqual(person.birthday, None, "Error: " + person.name + "'s birthday cannot be None!")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))    

            if person.death == "N/A":
                print(person.name + " has not died yet!")
                continue

            deathDaySplit = person.death.split(" ")
            deathDay = datetime.datetime(int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))        
            self.assertLess(birthday, deathDay, "Error: " + person.name + "'s death is before their birthday!")
    
    # US04 - Marriage before divorce
    def test_marr_before_div(self):
        for family in table[1]:
            if family.married == "N/A":
                print("Error: No marriage has occurred in this family!")
                continue

            if family.divorced == "N/A":
                print(family.husb_name + " and " + family.wife_name + " have not divorced!")
                continue

            if family.divorced != "N/A":    
                marriedSplit = family.married.split(" ")
                marriedDay = datetime.datetime(int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                divorcedSplit = family.divorced.split(" ")
                divorcedDay = datetime.datetime(int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))
                self.assertLess(marriedDay, divorcedDay, "Error: Divorced date cannot be before marriage date!")
    
    # US05 - Marriage before death
    def test_marr_before_death(self):
        return

    # US06 - Divorce before death
    def test_div_before_death(self):
        return

if __name__ == '__main__':
    unittest.main()