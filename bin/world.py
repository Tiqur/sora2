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

    # Search radius around 0, 0 for slime chunk clusters
    def _search(self, radius):
        half_radius = int(radius / 2);
        for z in range(-half_radius, half_radius):
            for x in range(-half_radius, half_radius):
                self._get_cluster(x, z, True);

    # Recursively search for nearby slime chunks within cluster and return dimensions
    def get_cluster(self, x, z, first=False):

        # If not slime chunk, exit
        if not self._is_slime_chunk(x, z): return;

        # Holds coordinats of checked chunks
        if not hasattr(self._is_slime_chunk, 'checked_chunks'):
            get_cluster.checked_chunks = [];

        # If first instance of class, clear coordinates
        if first:
            checked_chunks.checked_chunks = [];

        # Push self to checked chunks
        get_cluster.checked_chunks += {'x': x, 'x': z};

        print(len(get_cluster.checked_chunks));
        
        # Check sides 
        self._get_cluster(x+1, z);
        self._get_cluster(x-1, z);
        self._get_cluster(x, z+1);
        self._get_cluster(x, z-1);


            


    # For debugging
    def _print_map(self, radius):
        half_radius = int(radius / 2);
        for z in range(-half_radius, half_radius):
            for x in range(-half_radius, half_radius):
                print('■ ' if self._is_slime_chunk(x, z) else '□ ', end='');
            print('');
        
