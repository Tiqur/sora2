
# Emulate Java's random class for world generation
class Random:
    def __init__(self, seed=None):
        self._multiplier = hex(0x5DEECE66D);
        self._addend = hex(0xB);
        self._mask = (1 << 48) - 1;
        self._seed = seed;


    

