import csv
import os

file_path = 'database.csv'

def Is_Empty(file):
    # open ile in read mode
    with open(file, 'r') as readFile:
        #read first character
        paragraph = readFile.read()
        if paragraph.isspace() or not paragraph:
                return True
        return False

def Create_Header():
    header = ['Temperature', 'Water Level', 'Ammonia', 'Water pH', 'Battery Status', 'Battery Level']
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        #write the header
        writer.writerow(header)

def Write_Row(d1,d2,d3,d4,d5,d6):
    data = [d1,d2,d3,d4,d5,d6]
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        #write the data
        writer.writerow(data)


def Csv_Manager(tmp,wL,amm,pH,bS,bL):
    #read 11 rows in csv file, input is list of lists & elements are strings
    strData = read_file()
    #Shift to the left all
    for i in range(1,10):
        strData[i] = strData[i+1]
    #replace last element with incoming data but in string
    strData[10] = [str(tmp),str(wL),str(amm),str(pH),str(bS),str(bL)]
    #Save back to csv
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(strData)


def CheckNumRows():
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        numRows = len(list(reader))
    return numRows


def read_file():
    #read 11 rows in csv file, input is list of lists & elements are strings
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        strData = list(reader)
    return strData


def save_data(tmp, wL, amm, pH, bS, bL):
    try:
        if Is_Empty(file_path):
            Create_Header()

    except FileNotFoundError:
        Create_Header()

    #Check_N_Add(tmp,wL,amm,pH,bS,bL)
    numRows = CheckNumRows()
    if numRows <11:
        Write_Row(tmp,wL,amm,pH,bS,bL)
    else:
        Csv_Manager(tmp,wL,amm,pH,bS,bL)


    print("Data has been added to database")


