#!/usr/bin/env python2.7

import sys
import os

def separar_en_difonos(string):
    res = []
    primero = string[0]
    ultimo = string[-1]
    res.append("-"+primero)

    for i in range(len(string)-1):
        res.append(string[i]+string[i+1])

    res.append(ultimo+"-")

    return res

def main():
    string = sys.argv[1]
    # output_dir = sys.argv[2]

    pregunta = False

    if(string[-1] == '?'):
        pregunta = True
        string = string[:-1]


    difonos = separar_en_difonos(string)
    archivo = open("concatenar.praat", "w")

    # Creamos script de praat que abra todos los archivos necesarios y los seleccione
    for i, difono in enumerate(difonos):
         # Selecciono el difono
         archivo.write("Read from file: " + '"audios/difonos/' + str(difono) + '"' + "\n")

         # Renombro difono
         archivo.write("selectObject: " + str(difono) +  ' Rename: "difono' + str(i) +'"' + "\n" )

    # Ejecutamos el script de praat
    # os.system('praat concatenar.praat')

main()
