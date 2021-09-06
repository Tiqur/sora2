from bin.world import search;
import multiprocessing as mp;
import datetime, random, requests, json, os;

WORLDS = int(os.environ.get('WORLDS', 999999999999999));
THREADS = int(os.environ.get('THREADS', 4));
RADIUS = int(os.environ.get('RADIUS', 2500));
MIN_SIZE = int(os.environ.get('MIN_SIZE', 18));
SPACING = int(os.environ.get('SPACING', 3));

seeds_searched = 0;
thread_pool = [];

# Search random seed
def search_seed(seed):
    #start = datetime.datetime.now();
    print("Searching: " + str(seed));
    clusters = search(seed=seed, radius=RADIUS*2, min_size=MIN_SIZE, spacing=SPACING);
    #print(datetime.datetime.now() - start);

    # If cluster is found, POST to server
    if clusters:
        requests.post('http://localhost:3000/api', headers={'Content-type': 'application/json', 'Accept': 'text/plain'}, data=json.dumps(clusters));


print(f'Starting slime chunk finder...\nWorlds: {WORLDS}\nThreads: {THREADS}\nRadius: {RADIUS}\nMinimum chunk size: {MIN_SIZE}\nSpacing opitmization: {SPACING}\n');

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


