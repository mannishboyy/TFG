import csv
import glob
import pandas as pd
import os
import librosa
###########FUNCTIONS#########


# THIS FUNCTION RETURNS THE ON SET VALUES OF THE ORIGINAL PIECE TO COMPARE.
def o_file(o_filename):
    with open(o_filename, 'r') as original:
        value_original = []
        original_reader = csv.reader(original, dialect='excel')
        for row in original_reader:
            value_original.append(row[5])
            # print(row)
    return value_original

# THIS FUNCTION RETURNS THE ON SET VALUES TO COMPARE, BETWEEN DIFFERENT PIECES.
def x_file(x_filename):
    with open(x_filename, 'r') as original:
        values = []
        original_reader = csv.reader(original, dialect='excel')
        for linia in original_reader:
            break
        for row in original_reader:
            norm = float(row[5])
            values.append(float(row[5]) - norm)
            break
        for lin in original_reader:
            values.append(float(lin[5]) - norm)
    return values


def x_fileBE(file):
    min = float(originalValues[1])
    max = float(originalValues[-1])
    with open(file, 'r') as actual:
        actualReader = csv.reader(actual, dialect='excel')
        values = []
        for line in actualReader:
            break
        for lin in actualReader:
            norm = float(lin[5])
            values.append('0')
            break
        for li in actualReader:
            a = float(li[5]) - norm
            aNorm = (a-min)/(max - min)
            values.append(aNorm)
    return values


# Esta función crea los nuevos csv y añade la desviación del onset inicializada a 0
def generateFile(file, originalValues):
    ini = file.find('S')
    end = file.find('T')
    newName = file[ini-1:end]
    with open(file, 'r') as comparer, open('OnsetDeviationCsv/' + newName + '.csv', 'w', newline='') as newfile:
        comparerReader = csv.reader(comparer, dialect='excel')
        newfileWriter = csv.writer(newfile)
        newfileWriter.writerow(['O'])
        fila = 1
        next(comparerReader)
        for linia in comparerReader:
            if isinstance(float(linia[5]), float):
                norm = float(linia[5])
                newfileWriter.writerows(['0'])
                break
        for row in comparerReader:
            fila = fila + 1
            a = float(row[5]) - norm
            b = originalValues[fila]
            resultado = a - float(b)
            newfileWriter.writerow([resultado])
    comparer.close()
    newfile.close()


# Me clasifica a valor nominal la desviación
def ODNominal(file, column, nameNominal):
    with open(file, 'r') as reader:
        Nominal = []
        original_reader = csv.reader(reader, dialect='excel')
        next(original_reader)
        for row in original_reader:
            if float(row[column]) > 0.1:
                Nominal.append('adv')
            elif float(row[column]) < -0.1:
                Nominal.append('del')
            else:
                Nominal.append('none')
    csvAdd(file, Nominal, nameNominal)


# Añade columna al csv
def csvAdd(file, arrayNominal, nameNominal):
    df = pd.read_csv(file)
    df[nameNominal] = arrayNominal
    df.to_csv(file, index=False)

def completeFile(file):
    pos = file.find('-')
    ini = file.find('S')
    letter = file[pos+1:pos+2]
    filenameA = 'CsvFiles/' + file[ini:pos+1] + 'AT_nmat.csv'
    A = x_file(filenameA)
    filenameB = 'CsvFiles/' + file[ini:pos+1] + 'BT_nmat.csv'
    B = x_file(filenameB)
    filenameC = 'CsvFiles/' + file[ini:pos+1] + 'CT_nmat.csv'
    C = x_file(filenameC)
    pos = 0
    OD_1=[]
    OD_2=[]
    if letter == 'A':
        for x in A:
            OD_1.append(float(x)-float(B[pos]))
            OD_2.append(float(x) - float(C[pos]))
            pos = pos+1
        return OD_1, OD_2
    elif letter == 'B':
        for x in B:
            OD_1.append(float(x) - float(A[pos]))
            OD_2.append(float(x) - float(C[pos]))
            pos = pos + 1
        return OD_1, OD_2
    elif letter == 'C':
        for x in C:
            OD_1.append(float(x) - float(A[pos]))
            OD_2.append(float(x) - float(B[pos]))
            pos = pos + 1
        return OD_1, OD_2


#Vamos a normalizar todas las piezas respecto a los onsets de la pieza original
def completeFileBE(file):
    pos = file.find('-')
    ini = file.find('S')
    letter = file[pos+1:pos+2]
    filenameA = 'CsvFiles/' + file[ini:pos+1] + 'AT_nmat.csv'
    A = x_fileBE(filenameA)
    filenameB = 'CsvFiles/' + file[ini:pos+1] + 'BT_nmat.csv'
    B = x_fileBE(filenameB)
    filenameC = 'CsvFiles/' + file[ini:pos+1] + 'CT_nmat.csv'
    C = x_fileBE(filenameC)
    pos = 0
    OD_1=[]
    OD_2=[]
    if letter == 'A':
        for x in A:
            OD_1.append(float(x)-float(B[pos]))
            OD_2.append(float(x) - float(C[pos]))
            pos = pos+1
        return OD_1, OD_2
    elif letter == 'B':
        for x in B:
            OD_1.append(float(x) - float(A[pos]))
            OD_2.append(float(x) - float(C[pos]))
            pos = pos + 1
        return OD_1, OD_2
    elif letter == 'C':
        for x in C:
            OD_1.append(float(x) - float(A[pos]))
            OD_2.append(float(x) - float(B[pos]))
            pos = pos + 1
        return OD_1, OD_2


###########CODE##############

# ORIGINAL PIECE
o_filename = 'CsvFiles/Miniature1.csv'
# LIST OF FILES
all_files_nmat = glob.glob('CsvFiles/*T_nmat.csv')
# A FILES
files_a = glob.glob('CsvFiles/*AT_nmat.csv')
# B FILES
files_b = glob.glob('CsvFiles/*BT_nmat.csv')
# C FILES
files_c = glob.glob('CsvFiles/*CT_nmat.csv')
# New files
newFiles = glob.glob('OnsetDeviationCsv/*')

originalValues = o_file(o_filename)

for file in all_files_nmat:
    generateFile(file, originalValues)

# New files
newFiles = glob.glob('OnsetDeviationCsv/*')
for file in newFiles:
    ODNominal(file, 0, 'O_N')


for file in newFiles:
    OD_1, OD_2 = completeFile(file)
    pos = file.find('-')
    letter = file[pos + 1:pos + 2]
    if letter == 'A':
        csvAdd(file, OD_1, 'B')
        ODNominal(file, 2, 'B_Nom')
        csvAdd(file, OD_2, 'C')
        ODNominal(file, 4, 'C_Nom')
    elif letter == 'B':
        csvAdd(file, OD_1, 'A')
        ODNominal(file, 2, 'A_Nom')
        csvAdd(file, OD_2, 'C')
        ODNominal(file, 4, 'C_Nom')
    elif letter == 'C':
        csvAdd(file, OD_1, 'A')
        ODNominal(file, 2, 'A_Nom')
        csvAdd(file, OD_2, 'B')
        ODNominal(file, 4, 'B_Nom')

for file in newFiles:
    OriginalValuesBE = x_fileBE('CsvFiles/Miniature1.csv')
    OD_1, OD_2 = completeFileBE(file)
    pos = file.find('-')
    letter = file[pos + 1:pos + 2]
    csvAdd(file, OriginalValuesBE, 'O_BE')
    ODNominal(file, 6, 'O_BE_Nom')
    if letter == 'A':
        csvAdd(file, OD_1, 'B_BE')
        ODNominal(file, 8, 'B_BE_Nom')
        csvAdd(file, OD_2, 'C_BE')
        ODNominal(file, 10, 'C_BE_Nom')
    elif letter == 'B':
        csvAdd(file, OD_1, 'A_BE')
        ODNominal(file, 8, 'A_BE_Nom')
        csvAdd(file, OD_2, 'C_BE')
        ODNominal(file, 10, 'C_BE_Nom')
    elif letter == 'C':
        csvAdd(file, OD_1, 'A_BE')
        ODNominal(file, 8, 'A_BE_Nom')
        csvAdd(file, OD_2, 'B_BE')
        ODNominal(file, 10, 'B_BE_Nom')