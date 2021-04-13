import csv
import glob
import pandas as pd
import librosa

#THIS FUNCTION RETURNS THE ON SET VALUES OF THE ORIGINAL PIECE TO COMPARE.
def o_file(o_filename):
    with open(o_filename, 'r') as original:
        value_original = []
        original_reader = csv.reader(original, dialect='excel')
        for row in original_reader:
            value_original.append(row[5])
            #print(row)
    return value_original

#THIS FUNCTION RETURNS THE ON SET VALUES TO COMPARE, BETWEEN DIFFERENT PIECES.
def x_file(x_filename):
    with open(x_filename, 'r') as original:
        value_original = []
        original_reader = csv.reader(original, dialect='excel')
        for linia in original_reader:
            value_original.append(linia[5])
            break
        for row in original_reader:
            norm = float(row[5])
            value_original.append(float(row[5])-norm)
            break
        for lin in original_reader:
            value_original.append(float(lin[5]) - norm)
    return value_original

#THIS FUNCTION COMPARES THE GIVEN VALUES BETWEEN ALL OF THE FILES
def comp_file0(comp_filename, w_filename, value_original):
    with open(comp_filename, 'r') as compare, open(w_filename, 'w', newline='') as result:
        compare_reader = csv.reader(compare, dialect='excel')
        result_writer = csv.writer(result)
        result_writer.writerow(['OnSet desviation'])
        fila = 1
        next(compare_reader)
        for linia in compare_reader:
            if isinstance(float(linia[5]), float):
                norm = float(linia[5])
                result_writer.writerows(['0'])
                break
        for row in compare_reader:
            fila = fila+1
            a = float(row[5])-norm
            b = value_original[fila]
            resultado = a-float(b)
            result_writer.writerow([resultado])
#THIS FUNCTION MAKES COMPARATIONS BETWEEN THE ORIGINAL AND THE REST OF THE PIECES, AND CREATES THE NEW CSV FILES
def Norm0(o_filename,all_files_nmat,files_a,files_b,files_c):
    value_original = o_file(o_filename)
    for file in all_files_nmat:
        comp_file0(file, 'Resultados_0/'+file[9:12]+'_o-'+file[13:14]+'.csv',value_original)
    pos = 0
    for file in files_a:
        value_original = x_file(file)
        comp_file0(files_b[pos],'Resultados_0/'+file[9:12]+'_A-B.csv',value_original)
        comp_file0(files_c[pos], 'Resultados_0/'+file[9:12]+'_A-C.csv',value_original)
        pos =pos+1
    pos = 0
    for file in files_b:
        value_original = x_file(file)
        comp_file0(files_c[pos], 'Resultados_0/'+file[9:12]+'_B-C.csv',value_original)
        pos =pos+1

#aqui tenia la intención de haceer una normalizació pero creo que no tiene mucha logica
def NormBE(o_filename,all_files_nmat,files_a,files_b,files_c):
    value_original = o_file(o_filename)
    for file in all_files_nmat:
        comp_fileBE(file, 'Resultados_BE/'+file[9:12]+'_o-'+file[13:14]+'.csv',value_original)
    pos = 0
    for file in files_a:
        value_original = o_file(file)
        comp_fileBE(files_b[pos],'Resultados_BE/'+file[9:12]+'_A-B.csv',value_original)
        comp_fileBE(files_c[pos], 'Resultados_BE/'+file[9:12]+'_A-C.csv',value_original)
        pos =pos+1
    pos = 0
    for file in files_b:
        value_original = o_file(file)
        comp_fileBE(files_c[pos], 'Resultados_BE/'+file[9:12]+'_B-C.csv',value_original)
        pos =pos+1
def comp_fileBE(comp_filename, w_filename, value_original):
    with open(comp_filename, 'r') as compare, open(w_filename, 'w', newline='') as result:
        compare_reader = csv.reader(compare, dialect='excel')
        data = pd.read_csv(comp_filename, header=0)
        maxComp = data.at[144, 'Onset_s']
        result_writer = csv.writer(result)
        result_writer.writerow(['OnSet desviation'])
        fila = 1
        min = float(value_original[1])
        max = float(value_original[-1])
        next(compare_reader)
        for linia in compare_reader:
            if isinstance(float(linia[5]), float):
                norm = linia[5]
                result_writer.writerows(['0'])
                break
        for row in compare_reader:
            fila = fila+1
            a = float(row[5])-float(norm)
            a_normBE = (a-min)/(maxComp-min)
            b = float(value_original[fila])
            b_normBE = (b-min)/(max-min)
            resultado = a_normBE - b_normBE
            result_writer.writerow([resultado])

#ORIGINAL PIECE
o_filename = 'CsvFiles/Miniature1.csv'
#LIST OF FILES
all_files_nmat = glob.glob('CsvFiles/*T_nmat.csv')
# A FILES
files_a = glob.glob('CsvFiles/*AT_nmat.csv')
# B FILES
files_b = glob.glob('CsvFiles/*BT_nmat.csv')
# C FILES
files_c = glob.glob('CsvFiles/*CT_nmat.csv')

Norm0(o_filename,all_files_nmat,files_a,files_b,files_c)
#NormBE(o_filename,all_files_nmat,files_a,files_b,files_c)










