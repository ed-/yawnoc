class YawnocException(Exception):
    # Base class.
    pass

class GardenOfEden(YawnocException):
    # Board appears to be impossible to get to from anywhere.
    pass


class BadGuess(YawnocException):
    # Yawnoc.guess chose poorly along the way.
    pass


class Impossible(YawnocException):
    # This Alibi is out of possible Histories.
    pass
