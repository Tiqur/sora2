from bin.world import search;
import multiprocessing as mp;
import datetime, random, requests;

WORLDS = 1;
THREADS = 4;
RADIUS = 10000;
MIN_SIZE = 6;
SPACING = 3;

seeds_searched = 0;
thread_pool = [];

# Search random seed
def search_seed(seed):
    #start = datetime.datetime.now();
    print("Searching: " + str(seed));
    clusters = search(seed=seed, radius=RADIUS, min_size=MIN_SIZE, spacing=SPACING);
    #print(datetime.datetime.now() - start);

    # If cluster is found, POST to server
    if clusters:
        requests.post('http://149.28.75.54/api', data=str(clusters));



# Generate random seed
while seeds_searched < WORLDS:
    # Remove thread from pool if done executing
    for t in thread_pool:
        if not t.is_alive():
            thread_pool.remove(t);

    # Add thread to pool if len(thread_pool) < max THREADS
    if len(thread_pool) < THREADS:
        seeds_searched += 1;
        seed = random.randint(-9223372036854775808, 9223372036854775807);
        t = mp.Process(target=search_seed, args=(seed, ));
        thread_pool.append(t);
        t.start();


