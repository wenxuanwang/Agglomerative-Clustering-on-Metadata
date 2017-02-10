import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
import scipy.cluster.hierarchy as hcluster
import parse
import itertools

"""
Input Parameters
------------------------------------------------------------
"""
thresh_init = 12000000
file_path = "anon-lnfs-fs4.txt"
n_clusters_lo = 4
n_clusters_hi = 6

"""
------------------------------------------------------------
"""
# parse contents
snapshot_path = file_path
file_dict = parse.parser(snapshot_path)
n_samples = len(file_dict)
# obtain different permutations for further observation
input = ["file_id", "user_id", "group_id", "size_in_bytes", "creation_time",
         "modification_time", "block_size_in_bytes"]
input_list = itertools.permutations(input, 3)

# plotting
for single_input in input_list:
    x_axis, y_axis, z_data = single_input
    # label the units
    x_label = x_axis + ' (unit: s)' if 'time' in x_axis else x_axis
    y_label = y_axis + ' (unit: s)' if 'time' in y_axis else y_axis
    cbar_label = z_data + ' (unit: s)' if 'time' in z_data else z_data

    # binary search for appropiate threshold point
    thresh = thresh_init
    thresh_lo = 0
    thresh_hi = 3*thresh_init

    # initialize data lists
    x = []
    y = []
    z = []
    for file_id, file_data in file_dict.items():
        x.append(file_data[x_axis])
        y.append(file_data[y_axis])
        z.append(file_data[z_data])
    data = numpy.concatenate(([x], [y]))
    data = data.T
    # clustering with expected clusters
    while True:
        clusters = hcluster.fclusterdata(data, thresh, criterion="distance")
        count_clusters = len(set(clusters))
        if thresh_lo >= thresh_hi:
            break
        if count_clusters > n_clusters_hi:
            thresh_lo = thresh
            thresh = (thresh + thresh_hi) / 2
            continue
        if count_clusters < n_clusters_lo:
            thresh_hi = thresh
            thresh = (thresh_lo + thresh) / 2
            continue
        break

    n_clusters = []
    for i in clusters:
        if i not in n_clusters:
            n_clusters.append(i)

    shapes = ['o','h','D','v','^','s','<','*','>','H','.']
    cm = plt.cm.get_cmap('RdYlBu')
    legend_name_list = []
    for i in xrange(len(n_clusters)):
        points = []
        z2 = []
        for pos, j in enumerate(clusters):
            if j == n_clusters[i]:
                points.append(data[pos])
                z2.append(z[pos])
                legend_name_list.append(str(i))
        plt.scatter(*numpy.transpose(points), c=z2, s = 100, alpha=0.5,
                    marker = shapes[i], linewidths=0,label = i,cmap = cm)

    # set label
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # set title
    exp = 0
    thresh_decinal = float(thresh)
    while thresh_decinal > 2:
        thresh_decinal /= 10
        exp += 1
    thresh_standard_form = '%.2f * 10^%d' % (thresh_decinal,exp)
    title = "threshold: %s, number of clusters: %d" % (thresh_standard_form, len(set(clusters)))
    plot_title = plt.title(title)
    plot_title.set_position([.5, 1.05])

    # handle legends
    plt.legend(loc='upper left', markerscale = 0.6)
    ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=1)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=cm,
                           norm=mpl.colors.Normalize(vmin=min(z), vmax=max(z)))
    cbar.set_clim(min(z),max(z))
    cbar.set_label(cbar_label)

    # save images
    file_name = x_axis + ' ' + y_axis + ' ' + z_data
    plt.savefig(file_name)
    plt.clf()
