import re
import fileinput


class Parser(object):
    def parse(self):
        raise NotImplementedError('Subclass responsibility!')


class PitchParser(Parser):
    def parse(self, filename):
        points_size = 0
        point_index = -1
        print(filename)
        for line in fileinput.input(filename, inplace=True,  backup='.bak'):
            entre = False
            m = re.search('points: size = (.+?)$', str(line))
            if m:
                points_size = int(m.group(1))

            if points_size > 1:

                n = re.search('points \[(.+?)\]:', str(line))
                if n:
                    point_index = int(n.group(1))

                if point_index == points_size - 1 or point_index == points_size:
                    p = re.search('value = (.+?)$', str(line))
                    if p:
                        point_value = p.group(1)
                        point_value = float(point_value)
                        point_value += 45 * point_value / 100
                        # line = 'value = ' + str(point_value)
                        print('    value = ' + str(point_value))
                        entre = True
            if not entre:
                print(line, end="")

# if len(points) > 1:
#            points[-1] += 45 * points[-1] / 100
#            points[-2] += 45 * points[-2] / 100
#        elif len(points) == 1:
#            points[-1] += 45 * points[-1] / 100
