from bin.world import World;
import datetime;

start = datetime.datetime.now();

w = World(seed=4309860526323617207, radius=10000, min_size=10, spacing=3);
#w._print_map(20);



print(datetime.datetime.now() - start);
