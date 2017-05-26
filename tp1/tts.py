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

def main():
    string = sys.argv[1]
    output_name = sys.argv[2]

    pregunta = False

    if(string[-1] == '?'):
        pregunta = True
        string = string[:-1]


    difonos = separar_en_difonos(string)
    archivo = open("concatenar.praat", "w")
    os.system("mkdir tmp")
    i = 0
    # Creamos script de praat que abra todos los archivos necesarios y los seleccione
    while i < len(difonos):
        if(pregunta and 'A' in difonos[i]):
            # Extraccion del pitch
            os.system('praat scripts/extraer-pitch-track.praat ../audios/difonos/' + str(difonos[i]) + '.wav ../tmp/' + str(difonos[i]) + '.PitchTier 50 300')
            # Modifico Pitch
            pitch_parser = PitchParser()
            pitch_parser.parse(filename="tmp/" + str(difonos[i]) + '.PitchTier')
            # Resintetizamos audio
            os.system('praat scripts/reemplazar-pitch-track.praat ../audios/difonos/' + str(difonos[i]) +'.wav ../tmp/' + str(difonos[i]) + '.PitchTier ../tmp/' + str(difonos[i]) +'.wav 50 300')

        else:
            os.system("cp audios/difonos/" + str(difonos[i]) +".wav tmp/"   )

        # Selecciono el difono
        archivo.write("Read from file: " + '"tmp/' + str(difonos[i]) + '.wav"' + "\n")

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
        os.system('praat scripts/extraer-pitch-track.praat ../' + str(output_name) + ".wav ../tmp/" + str(output_name) + '.PitchTier 50 300')
        # Modificamos pitch
        pitch_parser = PitchParser()
        pitch_parser.parse(filename="tmp/" + str(output_name)+'.PitchTier')
        # Resintetizamos audio
        os.system('praat scripts/reemplazar-pitch-track.praat ../' + str(output_name) +'.wav ../tmp/' + str(output_name) + '.PitchTier ../'
                    + str(output_name) +'.wav 50 300')

    os.system("rm  concatenar.praat")
    os.system("rm -rf tmp/")
main()
