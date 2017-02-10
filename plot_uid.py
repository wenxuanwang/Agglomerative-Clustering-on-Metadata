import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import parse

mu, sigma = 100, 15
x = mu + sigma*np.random.randn(10000)

snapshot_path = "anon-lnfs-fs4.txt"
file_dict = parse.parser(snapshot_path)
x = []
for file_id, file_data in file_dict.items():
    x.append(file_data["modification_time"])

x = sorted(x)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, facecolor='green', alpha=0.75)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)

plt.grid(True)

plt.show()

