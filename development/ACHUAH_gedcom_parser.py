from datetime import date
from dateutil import parser
from prettytable import PrettyTable
import os
import unittest

familyTable = PrettyTable()
individuals = PrettyTable()

def calculateAge(birthDate, deathDate = None):
    # Convert birthdate to datetime object
    birth_obj = parser.parse(birthDate)
    if not deathDate:
        today = date.today()
        age = today.year - birth_obj.year - ((today.month, today.day) < (birth_obj.month, birth_obj.day))
    else:
        death_obj = parser.parse(deathDate)
        age = death_obj.year - birth_obj.year - ((death_obj.month, death_obj.day) < (birth_obj.month, birth_obj.day))

    return age

def createTables(file_name):
    # Opens gedcom file for reading
    f = open(file_name, "r")
    tagsLookup = [
        "INDI",
        "FAM",
        "NAME",
        "SEX",
        "BIRT",
        "DEAT",
        "FAMC",
        "FAMS",
        "MARR",
        "HUSB",
        "WIFE",
        "CHIL",
        "DIV",
        "DATE",
        "HEAD",
        "TRLR",
        "NOTE"
    ]

    ind_check = False
    dateTagToggle = "BIRT"
    birthDate = ""
    deathDate = ""
    currentIndividual = ""
    currentPersonName = ""
    currentFamily = ""
    children = []

    indi_id_lookup = {}
    family_id_lookup = {}

    # Column entries
    # Individual
    indi_ids = []
    names = []
    gender_list = []
    birthdays = []
    ages = []
    alive_list = []
    death_list = []

    # Family
    family_ids = []
    married_list = []
    divorce_list = []
    child_list = []
    husb_list = []
    husb_ids = []
    wife_list = []
    wife_ids = []

    while(True):
        line = f.readline()
        # If string is empty, means we are at the end of the file
        if not line:
            break
        _line = line.split()
        for tag in tagsLookup:
            if tag in _line:
                if tag == "INDI":
                    indi_ids.append(_line[1])
                    ind_check = True
                    currentIndividual = _line[1]
                elif tag == "FAM":
                    if len(child_list) != 0 and currentFamily != '':
                        family_id_lookup.setdefault(currentFamily, ', '.join(child_list))
                        child_list.clear()
                    elif len(child_list) == 0 and currentFamily != '':
                        family_id_lookup.setdefault(currentFamily, "N/A")
                    family_ids.append(_line[1])
                    currentFamily = _line[1]
                # Other tags
                else:
                    if ind_check:
                        args = ' '.join(_line[2:])
                        if args == "":
                            args = 'N/A'
                        if tag == "NAME":
                            names.append(args)
                            currentPersonName = args
                            indi_id_lookup[currentIndividual] = currentPersonName
                        elif tag == "SEX":
                            gender_list.append(args)
                        elif tag == "BIRT":
                            dateTagToggle = "BIRT"
                        elif tag == "DEAT":
                            dateTagToggle = "DEAT"
                        elif tag == "MARR":
                            dateTagToggle = "MARR"
                        elif tag == "DIV":
                            dateTagToggle = "DIV"
                        # This assumes both birt and deat tags come one after another
                        elif tag == "DATE":
                            if dateTagToggle == "BIRT":
                                birthDate = args
                                birthdays.append(args)
                                ages.append(calculateAge(birthDate))
                                alive_list.append("True")
                                death_list.append("N/A")
                            elif dateTagToggle == "DEAT":
                                deathDate = args
                                death_list[-1] = args
                                alive_list[-1] = "False"
                                ages[-1] = calculateAge(birthDate, deathDate)
                            elif dateTagToggle == "MARR":
                                married_list.append(args)
                                divorce_list.append("N/A")
                            elif dateTagToggle == "DIV":
                                divorce_list[-1] = args

                        elif tag == "HUSB":
                            if args in indi_id_lookup.keys():                                
                                husb_ids.append(args)
                                husb_list.append(indi_id_lookup.get(args))
                        elif tag == "WIFE":
                            if args in indi_id_lookup.keys():                                
                                wife_ids.append(args)
                                wife_list.append(indi_id_lookup.get(args))
                        elif tag == "CHIL":
                            child_list.append(args)

    family_id_lookup.setdefault(currentFamily, ', '.join(child_list))
    for k, v in family_id_lookup.items():
        children.append(v)

    individuals.add_column("ID", indi_ids)
    individuals.add_column("Name", names)
    individuals.add_column("Gender", gender_list)
    individuals.add_column("Birthday", birthdays)
    individuals.add_column("Alive", alive_list)
    individuals.add_column("Age", ages)
    individuals.add_column("Death", death_list)

    familyTable.add_column("ID", family_ids)
    familyTable.add_column("Married", married_list)
    familyTable.add_column("Divorced", divorce_list)
    familyTable.add_column("Husband ID", husb_ids)
    familyTable.add_column("Husband Name", husb_list)
    familyTable.add_column("Wife ID", wife_ids)
    familyTable.add_column("Wife Name", wife_list)
    familyTable.add_column("Children", children)

    # print(individuals)
    # print(familyTable)
    with open('output.txt', 'w') as w:
        w.write(str(individuals))
        w.write(str(familyTable))
    f.close()
    return

# createTables("ACHUAH_FAMILY.ged")