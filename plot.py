import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
import scipy.cluster.hierarchy as hcluster
import parse
import collections

def func():
    """
    Input Parameters
    ------------------------------------------------------------
    """
    thresh_init = 5000000
    file_path = "anon-lnfs-fs4.txt"
    n_clusters_lo = 10
    n_clusters_hi = 11

    bin = 6
    exclude_uid = True

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
    #input_list = itertools.permutations(input, 3)
    input_list = [["creation_time" , "modification_time", "user_id"]]


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
            # add normalization


            x.append(file_data[x_axis])
            y.append(file_data[y_axis])
            z.append(file_data[z_data])
        data = numpy.concatenate(([x], [y]))
        data = data.T

        x_ex = []
        y_ex = []
        z_ex = []
        if exclude_uid:
            for index in xrange(len(z)):
                if z[index] != 0:
                    x_ex.append(x[index])
                    y_ex.append(y[index])
                    z_ex.append(z[index])
            x = x_ex
            y = y_ex
            z = z_ex
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


    #   uid
        aux = []
        for i in xrange(bin):
            aux.append(i)

        counter = collections.Counter(z)
        most_common = []
        most_common = counter.most_common(bin)

        zz2 = []
        for i in xrange(len(z)):
            zz2.append(bin / 2)
        for i, (num, frequency) in enumerate(most_common):
            color = bin / 2
            if i % 2 == 0:
                color = aux.pop(0)
            else:
                color = aux.pop(len(aux)-1)
            for j in xrange(len(z)):
                if num == z[j]:
                    zz2[j] = color

        shapes = ['o','h','D','v','^','s','<','*','>','H','.']
        cm = plt.cm.get_cmap('RdYlBu')
        legend_name_list = []

        for i in xrange(len(n_clusters)):
            points = []
            z2 = []
            for pos, j in enumerate(clusters):
                if j == n_clusters[i]:
                    points.append(data[pos])
                    z2.append(zz2[pos])
                    legend_name_list.append(str(i))
            plt.scatter(*numpy.transpose(points), c=z2, s = 100, alpha=1,
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
        plt.legend(loc='lower right', markerscale = 0.6, title = 'clusters')
        ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=1)
        #cbar = mpl.colorbar.ColorbarBase(ax, cmap=cm,
        #                      norm=mpl.colors.Normalize(vmin=min(z), vmax=bin))

        bounds = numpy.linspace(0, bin, bin+1)
        norm = mpl.colors.BoundaryNorm(bounds, cm.N)
        cbar = mpl.colorbar.ColorbarBase(ax, cmap=cm, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds,
                                       format='%1i')

        cbar.set_clim(0,bin)
        cbar.set_label(cbar_label)

        # save images
        file_name = x_axis + ' ' + y_axis + ' ' + z_data
        #plt.savefig(file_name)
        plt.show()
        plt.clf()

if __name__ == "__main__":
    func()