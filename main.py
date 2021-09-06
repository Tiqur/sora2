from bin.world import search;
from colorama import Fore;
import multiprocessing as mp;
import datetime, random, os;

THREADS = int(os.environ.get('THREADS', 4));
RADIUS = int(os.environ.get('RADIUS', 2500));
MIN_SIZE = int(os.environ.get('MIN_SIZE', 18));
SPACING = int(os.environ.get('SPACING', 3));

# Search random seed
def search_seeds():
    while True:
        seed = random.randint(-9223372036854775808, 9223372036854775807);
        #start = datetime.datetime.now();
        print(f"{Fore.RESET}Searching: {Fore.YELLOW}{str(seed)}{Fore.RESET}");
        clusters = search(seed=seed, radius=RADIUS*2, min_size=MIN_SIZE, spacing=SPACING);
        #print(datetime.datetime.now() - start);

# Log starting message
print(f'{Fore.RESET}Starting slime chunk finder...\nThreads: {THREADS}\nRadius: {RADIUS}\nMinimum chunk size: {MIN_SIZE}\nSpacing optimization: {SPACING}\n');
    
# Start threads
for i in range(THREADS):
    mp.Process(target=search_seeds).start();
