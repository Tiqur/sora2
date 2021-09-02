from bin.random import Random;
import numpy as np

# Emulate world generation
class World:
    def __init__(self, seed=0, radius=20, min_size=8):
        self._seed = seed;
        self._min_size = min_size;
        self._random = Random();
        self._slime_chunks = [];
        self._search(radius);

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
    def _get_cluster(self, x, z, first=False):

        # If not slime chunk, exit
        if not self._is_slime_chunk(x, z): return;
        current_coords = {'x': x, 'z': z};

        # If not slime chunk andand does not include current coordinates ( chunk hasn't been checked )
        if self._is_slime_chunk(x, z) and not current_coords in self._slime_chunks:

            # If first instance of class, clear coordinates
            if first:
                self._slime_chunks.clear();

            # Push self to checked chunks
            self._slime_chunks.append(current_coords);
            
            # Check sides 
            self._get_cluster(x+1, z);
            self._get_cluster(x-1, z);
            self._get_cluster(x, z+1);
            self._get_cluster(x, z-1);

            # Add cluster to set if size >= min_size
            if len(self._slime_chunks) >= self._min_size and first:
                cluster_region = self._generate_cluster_region(self._slime_chunks);
                print(len(self._slime_chunks));

    # Generate 2D array representation of cluster
    def _generate_cluster_region(self, chunks):

        # Initialize bounding box
        top = bottom = chunks.pop().get('x');
        left = right = chunks.pop().get('z');

        # Find bounding box
        for c in chunks:
            left = min(c.get('z'), left);
            right = max(c.get('z'), right);
            top = min(c.get('x'), top);
            bottom = min(c.get('x'), bottom);

        # Bounding box dimensions
        width = right + 1 - left;
        height = top + 1 - bottom;

        # Create 2D representation of chunk cluster
        cluster = [[0]*height]*width;




    # For debugging
    def _print_map(self, radius):
        half_radius = int(radius / 2);
        for z in range(-half_radius, half_radius):
            for x in range(-half_radius, half_radius):
                print('■ ' if self._is_slime_chunk(x, z) else '□ ', end='');
            print('');
        
