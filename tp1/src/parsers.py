import re
import fileinput


class Parser(object):
    def parse(self, filename):
        raise NotImplementedError('Subclass responsibility!')


class PitchParser(Parser):
    def parse(self, filename):
        """" Metodo que parsea el archivo que contiene el pitch track y aumenta los ultimos valores para modificar la prosodia"""
        points_size = 0
        point_index = -1
        for line in fileinput.input(filename, inplace=True, backup='.bak'):
            entre = False
            m = re.search('points: size = (.+?)$', str(line))
            if m:
                points_size = int(m.group(1))

            if points_size > 1:

                n = re.search('points \[(.+?)\]:', str(line))
                if n:
                    point_index = int(n.group(1))

                # Para modificar el Pitch se toman los ultimos 6 valores del pitch y se los incrementa
                # en un valor de 25% con respecto a su valor anterior y de forma paulatina.
                if point_index >= points_size - 6:
                    p = re.search('value = (.+?)$', str(line))
                    if p:
                        point_value = p.group(1)
                        point_value = float(point_value)
                        point_value += (point_index * 25) * point_value / 100
                        print('    value = ' + str(point_value))
                        entre = True
            if not entre:
                print(line, end="")
