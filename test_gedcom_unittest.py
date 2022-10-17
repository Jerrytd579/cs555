import datetime
import unittest

import ACHUAH_gedcom_parser

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
            self.assertNotEqual(
                person.birthday, None, "Error: " + person.name + "'s birthday cannot be None!")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(
                int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
            self.assertLess(birthday, today,
                            "Error: Birthday cannot be before today")

            if person.death != "N/A":
                deathDaySplit = person.death.split(" ")
                deathDay = datetime.datetime(
                    int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))
                self.assertLess(deathDay, today,
                                "Error: deathday cannot be before today")

        for family in table[1]:
            for individual in table[0]:
                if (individual.id == family.husb_id or individual.id == family.wife_id):
                    if family.married != "N/A":
                        marriedSplit = family.married.split(" ")
                        marriedDay = datetime.datetime(
                            int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))
                        self.assertLess(
                            marriedDay, today, "Error: Married day cannot be before today")
                    if family.divorced != "N/A":
                        divorcedSplit = family.divorced.split(" ")
                        divorcedDay = datetime.datetime(
                            int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))
                        self.assertLess(
                            divorcedDay, today, "Error: Divorced day cannot be before today")
        print('Test US01 passed successfully!\n')

    # US02 - Birth before marriage
    def test_birth_before_marr(self):
        for family in table[1]:
            for individual in table[0]:
                if individual.id == family.husb_id or individual.id == family.wife_id:
                    if family.married == "N/A":
                        print(
                            "Error: Specified family does not have a marriage date!")
                        continue

                    marriedSplit = family.married.split(" ")
                    marriedDay = datetime.datetime(
                        int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                    self.assertNotEqual(
                        individual.birthday, None, "Error: " + individual.name + "'s birthday cannot be None")
                    birthDaySplit = individual.birthday.split(" ")
                    birthday = datetime.datetime(
                        int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))

                    self.assertLess(
                        birthday, marriedDay, "Error: Birthday must be before the married day!")

        print('Test US02 passed successfully!\n')

    # US03 - Birth before death
    def test_birth_before_death(self):
        for person in table[0]:
            self.assertNotEqual(
                person.birthday, None, "Error: " + person.name + "'s birthday cannot be None!")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(
                int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))

            if person.death == "N/A":
                print(person.name + " has not died yet!")
                continue

            deathDaySplit = person.death.split(" ")
            deathDay = datetime.datetime(
                int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))
            self.assertLess(birthday, deathDay, "Error: " +
                            person.name + "'s death is before their birthday!")
        print('Test US03 passed successfully!\n')

    # US04 - Marriage before divorce
    def test_marr_before_div(self):
        for family in table[1]:
            if family.married == "N/A":
                print("Error: Specified family does not have a marriage date!")
                continue

            if family.divorced == "N/A":
                print(family.husb_name + " and " +
                      family.wife_name + " have not divorced!")
                continue

            if family.divorced != "N/A":
                marriedSplit = family.married.split(" ")
                marriedDay = datetime.datetime(
                    int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                divorcedSplit = family.divorced.split(" ")
                divorcedDay = datetime.datetime(
                    int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))
                self.assertLess(
                    marriedDay, divorcedDay, "Error: Divorced date cannot be before marriage date!")
        print('Test US04 passed successfully!\n')

    # US05 - Marriage before death
    def test_marr_before_death(self):
        for family in table[1]:
            for individual in table[0]:
                if individual.id == family.husb_id or individual.id == family.wife_id:
                    if family.married == "N/A":
                        print(
                            "Error: Specified family does not have a marriage date!")
                        continue

                    marriedSplit = family.married.split(" ")
                    marriedDay = datetime.datetime(
                        int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                    if individual.death == "N/A":
                        print(individual.name + " has not died yet!")
                        continue

                    deathDaySplit = individual.death.split(" ")
                    deathDay = datetime.datetime(
                        int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))
                    self.assertLess(marriedDay, deathDay, "Error: " + individual.name +
                                    "'s death date cannot be before their marriage date!")
        print('Test US05 passed successfully!\n')

    # US06 - Divorce before death
    def test_div_before_death(self):
        for family in table[1]:
            for individual in table[0]:
                if individual.id == family.husb_id or individual.id == family.wife_id:
                    if family.divorced == "N/A":
                        print("Error: Specified family does not have a divorce date!")
                        continue

                    divorcedSplit = family.divorced.split(" ")
                    divorcedDay = datetime.datetime(
                        int(divorcedSplit[2]), month_dict[divorcedSplit[1]], int(divorcedSplit[0]))

                    if individual.death == "N/A":
                        print(individual.name + " has not died yet!")
                        continue

                    deathDaySplit = individual.death.split(" ")
                    deathDay = datetime.datetime(
                        int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))
                    self.assertLess(divorcedDay, deathDay, "Error: " + individual.name +
                                    "'s death date cannot be before their divorce date!")
        print('Test US06 passed successfully!\n')

    # US07 - Less than 150 years old
    def test_age_less_than_150(self):
        for individual in table[0]:
            self.assertIsNotNone(
                individual.age, "Error: individual does not have an age")
            self.assertNotEqual(individual.age, "N/A",
                                "Error: individual age cannot be N/A")
            self.assertLess(int(individual.age), 150,
                            "Error: person must be less than 150 years old")
        print('Test US07 passed successfully!\n')

    # US08 - Birth after marriage of parents
    def test_birth_after_parents_marry(self):
        for person in table[0]:
            self.assertNotEqual(
                person.birthday, None, "Error: " + person.name + "'s birthday cannot be None!")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(
                int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
            personid = person.id
            for family in table[1]:
                if personid in family.children:
                    marriedSplit = family.married.split(" ")
                    marriedDay = datetime.datetime(
                        int(marriedSplit[2]), month_dict[marriedSplit[1]], int(marriedSplit[0]))

                    self.assertGreater(
                        birthday, marriedDay, "Error: Person's birthday must be after parent's marriage.")
                else:
                    print("Error: Person has no parents")
                    return

        print('Test US08 passed successfully!\n')

    # US09 - Birth before death of parents
    def test_birth_before_death_of_parents(self):
        for person in table[0]:
            self.assertNotEqual(
                person.birthday, None, "Error: " + person.name + "'s birthday cannot be None!")
            birthDaySplit = person.birthday.split(" ")
            birthday = datetime.datetime(
                int(birthDaySplit[2]), month_dict[birthDaySplit[1]], int(birthDaySplit[0]))
            personid = person.id
            for family in table[1]:
                if personid in family.children:
                    man = family.husb_id
                    woman = family.wife_id
                    for parent in table[0]:
                        if parent.id == man or parent.id == woman:
                            if parent.alive == "True":
                                continue
                            else:
                                deathDaySplit = parent.death.split(" ")
                                deathDay = datetime.datetime(
                                    int(deathDaySplit[2]), month_dict[deathDaySplit[1]], int(deathDaySplit[0]))

                                self.assertLess(
                                    birthday, deathDay, "Error: Child's birthday is after the death of their parents!")
                else:
                    print("Error: Person has no parents")
                    return

        print('Test US09 passed successfully!\n')

    # US10 - Marriage after age 14 of parents
    def test_marriage_after_age_14(self):
        for family in table[1]:
            man = family.husb_id
            woman = family.wife_id
            for person in table[0]:
                if person.id == man or person.id == woman:
                    self.assertGreaterEqual(
                        person.age, 14, "Error: Person's age must be at least 14 in order to marry.")

        print("Test US10 passed successfully!\n")

    # US13 - Sibling Spacing
    def test_sibling_spacing(self):
        for family in table[1]:
            Children = family.children.split(", ")
            Birthdays = []
            for individual in table[0]:
                if individual.id in Children:
                    birthdaySplit = individual.birthday.split(" ")
                    birthDay = datetime.datetime(
                        int(birthdaySplit[2]), month_dict[birthdaySplit[1]], int(birthdaySplit[0])).date()
                    Birthdays.append(birthDay)
            for date1 in Birthdays:
                res = True
                idx = Birthdays.index(date1)
                for date2 in range(len(Birthdays)):
                    if (idx == date2):
                        continue
                    delta = date1 - Birthdays[date2]
                    if abs(delta.days) < 243 and not (delta.days == 0):
                        res = False
                self.assertEqual(res, True)
        print('Test US13 passed successfully!\n')

    # US14 - Multiple Births
    def test_multiple_births(self):
        for family in table[1]:
            Children = family.children.split(", ")
            Birthdays = []
            for individual in table[0]:
                if individual.id in Children:
                    birthdaySplit = individual.birthday.split(" ")
                    birthDay = datetime.datetime(
                        int(birthdaySplit[2]), month_dict[birthdaySplit[1]], int(birthdaySplit[0])).date()
                    Birthdays.append(birthDay)
            for date1 in Birthdays:
                birthdayCount = 0
                idx = Birthdays.index(date1)
                for date2 in range(len(Birthdays)):
                    if (idx == date2):
                        continue
                    if date1 == Birthdays[date2]:
                        birthdayCount = birthdayCount + 1
                self.assertLessEqual(birthdayCount, 5)
        print('Test US14 passed successfully!\n')


if __name__ == '__main__':
    unittest.main()
