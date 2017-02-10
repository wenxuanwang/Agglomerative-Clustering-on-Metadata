import time as time
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets.samples_generator import make_swiss_roll
import parse

snapshot_path = "anon-lnfs-fs4.txt"
file_dict = parse.parser(snapshot_path)
n_samples = len(file_dict)
x = []
y = []
z = []
for fileid ,filedata in file_dict.items():
    x.append(filedata['creation_time'])
    y.append(filedata['modification_time'])
    z.append(filedata['user_id'])
X = np.concatenate(([x], [y],[z]))
X = X.T

st = time.time()
ward = AgglomerativeClustering(n_clusters=6, linkage='ward').fit(X)
elapsed_time = time.time() - st
label = ward.labels_
print("time = %.2fs" % elapsed_time)
print("points = %i" % label.size)


fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    #ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
    #          'o', color=plt.cm.jet(float(l) / np.max(label + 1)))
    ax.plot3D(X[label == l, 0], X[label == l, 1], X[label == l, 2],
               'o', color=plt.cm.jet(float(l) / np.max(label + 1)))
ax.set_xlabel('creation time',fontsize = 10)
ax.set_ylabel('modification time',fontsize = 10)
ax.set_zlabel('uid',fontsize =10)

plt.title('creation, modification, uid')

plt.show()