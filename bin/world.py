from bin.random import jrand_int;
from numba import njit;
import numpy as np;
import copy;

# Organize chunks into histogram
def _max_histogram(row):
    result = [];
    top_val = 0;
    max_area = 0;
    area = 0;
    i = 0;

    while (i < len(row)):
        if (len(result) == 0) or (row[result[-1]] <= row[i]):
            result.append(i);
            i += 1;
        else:
            top_val = row[result.pop()];
            area = top_val * i;
            if (len(result)): area = top_val * (i - result[-1] - 1);
            max_area = max(area, max_area);

    while (len(result)):
        top_val = row[result.pop()]
        area = top_val * i
        if (len(result)): area = top_val * (i - result[-1] - 1)
        max_area = max(area, max_area)

    return max_area


# Find largest rect in submatrix histogram and return dimensions
def _find_largest_rect(histogram):
    result = _max_histogram(histogram[0])

    for i in range(1, len(histogram)):
        for j in range(len(histogram[i])):
            if (histogram[i][j]): histogram[i][j] += histogram[i - 1][j];

        result = max(result, _max_histogram(histogram[i]));

    return result


def _generate_bounding_box(chunks):
    
    # Initialize bounding box
    left = right = chunks[0][0];
    top = bottom = chunks[0][1];

    # Find bounding box
    for c in chunks:
        left = min(c[0], left);
        right = max(c[0], right);
        top = max(c[1], top);
        bottom = min(c[1], bottom);

    return (left, right, top, bottom);

# Generate 2D array representation of cluster
def _generate_cluster_region(bounding_box, chunks):

    left = bounding_box[0];
    right = bounding_box[1];
    top = bounding_box[2];
    bottom = bounding_box[3];

    # Bounding box dimensions
    width = right + 1 - left;
    height = top + 1 - bottom;

    # Initialize 2D array
    cluster_region = [[0 for i in range(width)] for j in range(height)]

    # Create 2D representation of chunk cluster_region
    for z in range(height):
        for x in range(width):
            c = (x+left, z+bottom)
            cluster_region[z][x] = c in chunks;

    return cluster_region;


# Determine if there is a slime chunk at x, z
@njit(fastmath=True)
def _is_slime_chunk(xPosition, zPosition, seed):
    # Set seed and location
    seed = (
      np.long(seed) +
      np.int32(xPosition * xPosition * 0x4c1906) +
      np.int32(xPosition * 0x5ac0db) +
      np.int32(zPosition * zPosition) * 0x4307a7 +
      np.int32(zPosition * 0x5f24f) ^ 0x3ad8025f
    );

    # Determine if slime chunk
    return jrand_int(seed, 10) == 0;


# Recursively search for nearby slime chunks within cluster and return dimensions
def _get_cluster(x, z, min_size, seed, slime_chunks, first=False):

    # If not slime chunk, exit
    if not _is_slime_chunk(x, z, seed): return;
    current_coords = (x, z);

    # If not slime chunk andand does not include current coordinates ( chunk hasn't been checked )
    if _is_slime_chunk(x, z, seed) and not current_coords in slime_chunks:

        # If first instance of class, clear coordinates
        if first:
            slime_chunks.clear();

        # Push self to checked chunks
        slime_chunks.append(current_coords);
        
        # Check sides 
        _get_cluster(x+1, z, min_size, seed, slime_chunks);
        _get_cluster(x-1, z, min_size, seed, slime_chunks);
        _get_cluster(x, z+1, min_size, seed, slime_chunks);
        _get_cluster(x, z-1, min_size, seed, slime_chunks);

        # Add cluster to set if size >= min_size
        if len(slime_chunks) >= min_size and first:
            bounding_box = _generate_bounding_box(slime_chunks);
            cluster_region = _generate_cluster_region(bounding_box, slime_chunks);
            largest_rect_size = _find_largest_rect(copy.deepcopy(cluster_region));

            if largest_rect_size > min_size:
                center_coordinates = (int((bounding_box[0] + bounding_box[1]) / 2) << 4, int((bounding_box[2] + bounding_box[3]) / 2) << 4);
                repr = '-'.join([''.join([('1' if r else '0') for r in c]) for c in cluster_region]);
                return {'seed': seed, 'chunks': [{'x': c[0], 'z': c[1]} for c in slime_chunks], 'coords': center_coordinates, 'repr': repr, 'size': largest_rect_size};
                _print_cluster_region(cluster_region);

# Search and return slime chunk clusters for seed
def search(seed=0, radius=20, min_size=8, spacing=1):
    half_radius = int(radius / 2);
    clusters = [];

    # Search radius around 0, 0
    for z in range(-half_radius, half_radius, spacing):
        for x in range(-half_radius, half_radius, spacing):
            cluster = _get_cluster(x, z, min_size, seed, [], True);
            if cluster: clusters.append(cluster);

    return clusters;


# Print cluster region
def _print_cluster_region(cluster_region):
    for z in cluster_region:
        for x in z:
            print('■ ' if x else '□ ', end='');
        print("");

# Print all slime chunks in radius
def _print_map(radius):
    half_radius = int(radius / 2);
    for z in range(-half_radius, half_radius):
        for x in range(-half_radius, half_radius):
            print('■ ' if _is_slime_chunk(x, z) else '□ ', end='');
        print('');
