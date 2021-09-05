from bin.world import search;
import datetime, random;

# Search random seed
def search_seed(seed):
    start = datetime.datetime.now();
    print("Searching: " + str(seed));
    clusters = search(seed=seed, radius=10000, min_size=10, spacing=3);
    print(datetime.datetime.now() - start);
    # If cluster is found, POST to server



# Generate random seed
seed = random.randint(-9223372036854775808, 9223372036854775807);
search_seed(seed);
