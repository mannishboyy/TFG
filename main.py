import csv
import glob



def o_file(o_filename):
    with open(o_filename, 'r') as original:
        value_original = []
        original_reader = csv.reader(original)
        for row in original_reader:
            value_original.append(row[5])
            #print(row)
    return value_original

def comp_file(comp_filename, w_filename):
    with open(comp_filename, 'r') as compare, open(w_filename, 'w', newline='') as result:
        compare_reader = csv.reader(compare)
        result_writer = csv.writer(result)
        result_writer.writerow(['OnSet desviation'])
        fila = 1
        next(compare_reader)
        for linia in compare_reader:
            if isinstance(float(linia[5]), float):
                norm = linia[5]
                result_writer.writerows(['0'])
                break
        for row in compare_reader:
            fila = fila+1
            a = float(row[5])-float(norm)
            b = value_original[fila]
            resultado = a-float(b)
            result_writer.writerow([resultado])



o_filename = 'CsvFiles/Miniature1.csv'
all_files_nmat = glob.glob('CsvFiles/*T_nmat.csv')
files_a = glob.glob('CsvFiles/*AT_nmat.csv')
files_b = glob.glob('CsvFiles/*BT_nmat.csv')
files_c = glob.glob('CsvFiles/*CT_nmat.csv')
value_original = o_file(o_filename)
for file in all_files_nmat:
    comp_file(file, 'Resultados/'+file[9:12]+'_o-'+file[13:14])
pos = 0
for file in files_a:
    value_original = o_file(file)
    comp_file(files_b[pos],'Resultados/'+file[9:12]+'_A-B')
    comp_file(files_c[pos], 'Resultados/'+file[9:12]+'_A-C')
    pos =pos+1
pos = 0
for file in files_b:
    value_original = o_file(file)
    comp_file(files_c[pos], 'Resultados/'+file[9:12]+'_B-C')
    pos =pos+1











