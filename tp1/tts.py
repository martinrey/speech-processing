#!/usr/bin/env python2.7

from parser import PitchParser
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

def limpiar():
    os.system("rm *.PitchTier")
    os.system("rm *.bak")
    os.system("rm concatenar.praat")

def main():
    string = sys.argv[1]
    output_name = sys.argv[2]

    pregunta = False

    if(string[-1] == '?'):
        pregunta = True
        string = string[:-1]


    difonos = separar_en_difonos(string)
    archivo = open("concatenar.praat", "w")
    i = 0
    # Creamos script de praat que abra todos los archivos necesarios y los seleccione
    while i < len(difonos):
        # if(pregunta and 'A' in difono):
        #     # Extraccion del pitch
        #     os.system('praat ../scripts/extraer-pitch-track.praat' + str(difono) + '.wav ' + str(difono) + '.PitchTier 50 300')
        #     # Modifico Pitch
        #

         # Selecciono el difono
         archivo.write("Read from file: " + '"audios/difonos/' + str(difonos[i]) + '.wav"' + "\n")

         # Renombro difono
         archivo.write('selectObject: "Sound '+ str(difonos[i]) + '"' + "\n")
         archivo.write('Rename: "difono' + str(i) +'"' + "\n" )
         i += 1
    # Selecciono todos los archivos
    archivo.write("select Sound difono0\n")
    i = 1
    while(i<len(difonos)):
        archivo.write("plus Sound difono"+str(i)+"\n")
        i += 1

    # Concateno todos los archivos abiertos
    archivo.write("Concatenate recoverably\n")

    # Selecciono el archivo concatenado
    archivo.write("select Sound chain\n")


    # Guardo el audio generado
    archivo.write('Save as WAV file: "' + str(output_name) + '.wav"')

    archivo.close()

    #  Ejecutamos el script de praat
    os.system('praat concatenar.praat')

    if(pregunta):
        # Extraemos pitch
        os.system('praat scripts/extraer-pitch-track.praat ../' + str(output_name) + ".wav ../" + str(output_name) + '.PitchTier 50 300')
        # Modificamos pitch
        pitch_parser = PitchParser()
        pitch_parser.parse(filename=str(output_name)+'.PitchTier')
        # Resintetizamos audio
        os.system('praat scripts/reemplazar-pitch-track.praat ../' + str(output_name) +'.wav ../' + str(output_name) + '.PitchTier ../'
                    + str(output_name) +'.wav 50 300')
        limpiar()
    else:
        os.system("rm concatenar.praat")
main()
