from pickle import TRUE
from prettytable import PrettyTable

familyTable = PrettyTable()
individuals = PrettyTable()

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

    check = TRUE
    

    # Column entries
    ids = []
    names = []
    gender_list = []
    birthdays = []
    alive_list = []
    children = []

    while(True):
        line = f.readline()
        # If string is empty, means we are at the end of the file
        if not line:
            break
        _line = line.split()
        for tag in tagsLookup:
            if tag in _line:
                if tag == "INDI":
                    ids.append(_line[1])

                    return
                elif tag == "FAM":
                    return
                # Other tags
                else:
                    args = ' '.join(_line[2:])
                    if args == "":
                        return
                    if tag == "NAME":
                        return
                    elif tag == "SEX":
                        return
                    elif tag == "BIRT":
                        return
                    elif tag == "DEAT":
                        return
                    elif tag == "MARR":
                        return
                    elif tag == "DATE":
                        return
                    elif tag == "HUSB":
                        return
                    elif tag == "WIFE":
                        return
                    elif tag == "CHIL":
                        return

    individuals.add_column("ID")
    individuals.add_column("Name")
    individuals.add_column("Gender")
    individuals.add_column("Birthday")
    individuals.add_column("Alive")

    f.close()
    return

createTables("ACHUAH_FAMILY.ged")