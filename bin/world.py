from bin.random import Random;
import numpy as np

# Emulate world generation
class World:
    def __init__(self, seed):
        self._seed = seed;
        self._random = Random();

    def _is_slime_chunk(self, xPosition, zPosition):
        self._random.set_seed(
          np.int32(self._seed) +
          np.int32(xPosition * xPosition * 0x4c1906) +
          np.int32(xPosition * 0x5ac0db) +
          np.int32(zPosition * zPosition) * 0x4307a7 +
          np.int32(zPosition * 0x5f24f) ^ 0x3ad8025f
        );

        return self._random.next_int(10) == 0;
