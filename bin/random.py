from numba import njit;
import numpy as np;


MULTIPLIER = 0x5DEECE66D;
ADDEND = 0xB;
MASK = (1 << 48) - 1;


@njit(fastmath=True)
# Scramble initial seed
def _initial_scramble(seed):
    return (seed ^ MULTIPLIER) & MASK;

@njit(fastmath=True)
# Generate next psuedo random number
def _next(seed, bits):
    temp_seed = np.long(np.long(seed) * MULTIPLIER + ADDEND) & MASK;
    return (temp_seed >> (48 - bits));

@njit(fastmath=True)
# Emulate Java's random class for world generation
def jrand_int(seed, n=32):
    # Set the seed of the random number generator
    scrambled_seed = _initial_scramble(seed);

    # Generate next pseudorandom int ( public )
    if (n <= 0):
        raise Exception('n must be positive');

    # If n is a power of 2
    if (n & -n) == n:
        return ((n * _next(scrambled_seed, 31)) >> 31);

    condition = True;
    while condition:
        bits = _next(scrambled_seed, 31);
        val = bits % n;
        condition = bits - val + (n-1) < 0;

    return val;


