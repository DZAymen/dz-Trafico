
class Converter:

    def tokmh(self, speed):
        return int(round(speed * 3.6))

    def toms(self, speed):
        return int(round(speed / 3.6))