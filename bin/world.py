from bin.random import Random;
import numpy as np

# Emulate world generation
class World:
    def __init__(self, seed):
        self._seed = seed;
        self._random = Random();

    # Determine if there is a slime chunk at x, z
    def _is_slime_chunk(self, xPosition, zPosition):
        # Set seed and location
        self._random.set_seed(
          np.int32(self._seed) +
          np.int32(xPosition * xPosition * 0x4c1906) +
          np.int32(xPosition * 0x5ac0db) +
          np.int32(zPosition * zPosition) * 0x4307a7 +
          np.int32(zPosition * 0x5f24f) ^ 0x3ad8025f
        );

        # Determine if slime chunk
        return self._random.next_int(10) == 0;

    # For debugging
    def _print_map(self, radius):
        half_radius = int(radius / 2);
        for x in range(-half_radius, half_radius):
            for z in range(-half_radius, half_radius):
                print('■ ' if self._is_slime_chunk(x, z) else '□ ', end='');
            print('');
        
