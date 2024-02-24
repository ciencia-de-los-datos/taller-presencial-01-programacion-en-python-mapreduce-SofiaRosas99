import glob # permite leer el contenido de directorios
import fileinput #permite iterar y operar en archivos

def load_input(input_directory):
    sequence=[] #crear una lista vacia
    filenames = glob.glob(input_directory + "/*") #regresa el nombre del archivo
    with fileinput.input (files=filenames) as f: #f es un obj que apunta a los archivos, se crea un objeto que maneja los archivo en disco llamado f, f contiene un iterador por dentro
        for line in f:
            sequence.append((fileinput.filename(),line)) #agregar a la lista 


    return sequence


def mapper(sequence):
    new_sequence = []
    for _, text in sequence:
        words = text.rstrip().split()
        for word in words:
            word = word.replace(",","")
            word = word.replace(".","")
            word = word.lower()
            new_sequence.append((word, 1))
    return new_sequence

def shuffle_and_sort(sequence):
    sorted_sequence= sorted (sequence, key=lambda x: x[0])
    return sorted_sequence

def reducer(sequence):

    diccionario = {}
    for key, value in sequence:
        if key not in diccionario.keys():
            diccionario[key] = 0
        diccionario[key] += value
    
    new_sequence = []
    for key, value in diccionario.items():
        tupla = (key, value)
        new_sequence.append(tupla)

    return new_sequence


import os.path

def create_output_directory(output_directory):
    if os.path.exists(output_directory): #retorna verdadero si el directorio existe
        raise FileExistsError(f"The directory '{output_directory}' already exists.")
    os.makedirs(output_directory)


def save_output(output_directory, sequence):
    with open(output_directory + "/part-00000", "w") as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    with open(output_directory + "/_SUCCESS", "w") as file:
        file.write("")



def job(input_directory, output_directory):
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_output_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)

if __name__ == "__main__":
    job(
      "input",
      "output",
    )
