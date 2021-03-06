from ipdb import set_trace
from numpy import *
Debug = False

'''
bin_info: x_min, x_max, bins
'''
def binning(x, bin_info):
    x_min, x_max, bins = bin_info

    y = floor( (x- x_min) / (x_max - x_min) * bins)

    y[y < 0] = float('nan')
    y[y >= bins] = float('nan')

    return y

'''
partition x into many bins,
and compute the average of y for each bin
'''
def binning_xy(x, bin_info, ys):
    x_min, x_max, bins = bin_info
    in_range = (x_min <= x) & (x < x_max)
    print '%.2f data points in range' % (sum(in_range) / (len(in_range) + 0.0))

    bin_x = binning(x, bin_info)
    centers = bin_centers(bin_info)

    count_x = zeros(bins)
    for i in range(bins):
        count_x[i] = sum(bin_x == i)

    values = []
    std_values = []

    for y in ys:
        vy = zeros(bins)
        std_y = zeros(bins)
        for i in range(bins):
            vy[i] = mean(y[bin_x == i])
            if Debug:
                z = y[bin_x == i]
                r = randint(0, 2, size(z)) == 1
                print len(r), mean(z[r]), mean(z[~r])

            std_y[i] = std(y[bin_x == i]) / sqrt(sum(bin_x == i))
        values.append(vy)
        std_values.append(std_y)

    return centers, count_x, values, std_values


'''
return the center of the bins
'''
def bin_centers(bin_info):
    x_min, x_max, bins = bin_info
    w = (x_max - x_min) / bins

    return x_min + w/2 + w * arange(bins)
