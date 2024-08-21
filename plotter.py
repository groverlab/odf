import numpy, sys, matplotlib.pyplot as plt, scipy.signal, json

r = json.load(open(sys.argv[1], "r"))

start = float(r["start_time"])
stop = float(r["stop_time"])
data = r["data"]

# data = numpy.loadtxt(sys.argv[1], skiprows=10, )
# stat = open(sys.argv[1][:-8]+"STAT.txt").read()
# start = float(stat.split("\n")[0])
# stop = float(stat.split("\n")[1])
duration = stop-start
points = len(data)
times = numpy.linspace(0, duration, points)
smooth = scipy.signal.savgol_filter(data, 20, 3)
fig, ax = plt.subplots(1, 1, figsize=(10, 3))
ax.plot(times, data)
# ax.plot(times, smooth)
# plt.yscale("log")
# ax.set_xlim(left=0, right=3.5e6)
# ax.set_ylim(bottom=13000, top=15500)
# plt.title(sys.argv[1])
plt.xlabel("Time (s)")
plt.ylabel("Light intensity (arbitrary)")
fig.tight_layout()
fig.savefig("out.png")
plt.show()