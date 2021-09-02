
# Emulate Java's random class for world generation
class Random:
    def __init__(self):
        self._multiplier = 0x5DEECE66D;
        self._addend = 0xB;
        self._mask = (1 << 48) - 1;
        self._seed = 0;

    # Scramble initial seed
    def _initial_scramble(self, seed):
        return (seed ^ self._multiplier) & self._mask;

    # Generate next psuedo random number
    def _next(self, bits):
        self._seed = (self._seed * self._multiplier + self._addend) & self._mask;
        return (self._seed >> (48 - bits));

    # Set the seed of the random number generator
    def set_seed(self, seed):
        self._seed = self._initial_scramble(seed);

    # Generate next pseudorandom int ( public )
    def next_int(self, n=32):
        # Make sure n is positive
        if (n <= 0):
            raise Exception('n must be positive');

        # If n is a power of 2
        if (n & -n) == n:
            return ((n * self._next(31)) >> 31);

        condition = True;
        while condition:
            bits = self._next(31);
            val = bits % n;
            condition = bits - val + (n-1) < 0;

        return val;




            
