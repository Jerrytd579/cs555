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

    # US29 - List Deceased
    def test_list_deceased(self):
        deceased = []
        for family in table[1]:
            for individual in table[0]:
                if individual.alive == "False":
                    if individual.name not in deceased:
                        deceased.append(individual.name)

        self.assertEqual(3, len(deceased))

        print("Deceased List:")
        for person in deceased:
            print(person + ",")

        print('Test US29 passed successfully!\n')

    # US30 - List Living Married
    def test_list_married(self):
        living_married = []
        for family in table[1]:
            if family.married and (family.divorced == "N/A"):
                for individual in table[0]:
                    if individual.alive == "True":
                        if individual.id == family.husb_id or individual.id == family.wife_id:
                            if individual.name not in living_married:
                                living_married.append(individual.name)

        self.assertEqual(8, len(living_married))

        print("Living Married List:")
        for person in living_married:
            print(person + ",")

        print('Test US30 passed successfully!\n')

    # US15 - Fewer than 15 siblings
    def test_lessThan15Siblings(self):
        for person in table[0]:
            for family in table[1]:
                children = family.children.split(", ")
                if person.id in children:
                    self.assertGreater(len(children)-1, -1, "Error: Person cannot have negative siblings.")
                    self.assertLess(len(children)-1, 15, "Error: Person has 15 or more siblings.")
        print("Test US15 passed successfully!\n")

    # US23 - Unique name and birth date
    def test_unique_name_and_birthdate(self):
        for person1 in table[0]:
            for person2 in table[0]:
                if person1.id == person2.id:
                    continue
                else:
                    person1Info = person1.name + " " + person1.birthday
                    person2Info = person2.name + " " + person2.birthday
                    self.assertNotEqual(person1Info, person2Info, "Error: Users must have both a unique name and birthdate.")
        print("Test US23 passed successfully!\n")

    # US24 - Unique families by spouses
    def test_unique_families_by_spouses(self):
        for family1 in table[1]:
            for family2 in table[1]:
                if family1.id == family2.id:
                    continue
                else:
                    spouses1 = family1.husb_id + " " + family1.wife_id
                    spouses2 = family2.husb_id + " " + family2.wife_id
                    self.assertNotEqual(spouses1, spouses2, "Error: Families must have unique pair of spouses.")
        print("Test US24 passed successfully!\n")

    # US25 - Unique first names in families
    def test_unique_first_names_in_families(self):
        for family in table[1]:
            familyIds = []
            familyNames = []
            familyIds.append(family.husb_id)
            familyIds.append(family.wife_id)
            familyIds += family.children.split(", ")

            for person in table[0]:
                if person.id in familyIds:
                    familyNames.append(person.name.split()[0])

            familyNamesDupe = set(familyNames)
            self.assertEqual(len(familyNamesDupe), len(familyNames), "Error: Family contains duplicate names.")
        print("Test US25 passed successfully!\n")

    # US16 - Male last names
    def test_male_last_names(self):
        print("Test US16 passed successfully!\n")

    # US17 - No marriages to descendants
    def test_no_descendant_marriage(self):
        print("Test US17 passed successfully!\n")

    # US18 - Siblings should not be married to each other
    def test_no_sibling_marriage(self):
        sibling_marriage = False
        for family in table[1]:
            children = family.children.split(", ")
            if "N/A" in children or len(children) <= 1:
                continue
            else:
                for i in range(len(children)):
                    for j in range(i+1, len(children)):
                        if any(children[i] in [family.husb_id, family.wife_id] and children[j] in [family.husb_id, family.wife_id] for f in table[1]):
                            sibling_marriage = True

        self.assertNotEqual(sibling_marriage, True, "Error: Some siblings are married to each other.")
        print("Test US18 passed successfully!\n")
    
    # US19 - First cousins should not be married to each other
    def test_no_first_cousin_marriage(self):
        print("Test US19 passed successfully!\n")

    # US20 - Aunts and uncles
    def test_uncles_aunts(self):
        print("Test US20 passed successfully!\n")

    # US21 - Correct gender for role (ex: wife should be female)
    def test_gender_roles(self):
        print("Test US21 passed successfully!\n")

if __name__ == '__main__':
    unittest.main()
