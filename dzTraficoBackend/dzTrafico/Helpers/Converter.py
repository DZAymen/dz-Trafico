
class Converter:

    @staticmethod
    def tokmh(speed):
        return int(round(speed * 3.6))

    @staticmethod
    def toms(speed):
        return int(round(speed / 3.6))