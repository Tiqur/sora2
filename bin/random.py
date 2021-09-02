
# Emulate Java's random class for world generation
class Random:
    def __init__(self, seed=None):
        self._multiplier = 0x5DEECE66D;
        self._addend = 0xB;
        self._mask = (1 << 48) - 1;
        self._seed = seed;

    def test(self):
        print(self._seed);
        print(self._multiplier);
        print(self._addend);
        print(self._mask);

    # Set the seed of the random number generator
    def set_seed(self, seed):
        self._seed = seed;

    # Scramble initial seed
    def initial_scramble(seed):
        return (seed ^ this._multiplier) & this._mask;

    # Generate next psuedo random number
    def next(bits):
        this._seed = (this._seed * this._multiplier + this._addend) & this._mask;
        return (this._seed >> (48 - bits));




    

