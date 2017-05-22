import re


class Parser(object):
    def parse(self):
        raise NotImplementedError('Subclass responsibility!')


class PitchParser(Parser):
    def parse(self):
        points = []
        with open('lakAsa.PitchTier', 'rb') as pitch_file:
            for line in pitch_file:
                m = re.search('value = (.+?)$', str(line))
                if m:
                    point_value = m.group(1)
                    points.append(float(point_value[:-3]))

        if len(points) > 1:
            points[-1] += 45 * points[-1] / 100
            points[-2] += 45 * points[-2] / 100
        elif len(points) == 1:
            points[-1] += 45 * points[-1] / 100
