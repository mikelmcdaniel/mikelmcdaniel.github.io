import collections
import csv
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors


def load_approx_ops_csv(csv_filename):
    approx_ops_base_2 = collections.defaultdict(dict)
    approx_ops_base_e = collections.defaultdict(dict)
    # with open("/home/mikel/Desktop/output_4.csv", "r") as f:
    with open(csv_filename, "r") as f:
        for row in csv.DictReader(f):
            num_elements = int(row["num_elements"])
            num_buckets = int(row["num_buckets"])
            if num_buckets < 2:
                continue
            approx_ops_base_2[num_elements][num_buckets] = float(row["approx_ops_base_2"]) / num_elements
            approx_ops_base_e[num_elements][num_buckets] = float(row["approx_ops_base_e"]) / num_elements
    return approx_ops_base_2, approx_ops_base_e


def plot(approx_ops, out_filename, title=None):
    min_x = min(num_elements for num_elements in approx_ops)
    max_x = max(num_elements for num_elements in approx_ops)
    min_y = min(num_buckets for sub_dict in approx_ops.values() for num_buckets in sub_dict)
    max_y = max(num_buckets for sub_dict in approx_ops.values() for num_buckets in sub_dict)
    min_val = min(val for sub_dict in approx_ops.values() for val in sub_dict.values())
    max_val = max(val for sub_dict in approx_ops.values() for val in sub_dict.values())
    num_elementss = sorted(num_elements for num_elements in approx_ops)
    num_bucketss = sorted(set(num_buckets for sub_dict in approx_ops.values() for num_buckets in sub_dict))
    width = len(num_elementss)
    height = len(num_bucketss)
    z = np.zeros((height, width))
    for x, num_elements in enumerate(num_elementss):
        for y, num_buckets in enumerate(num_bucketss):
            try:
                z[y, x] = approx_ops[num_elements][num_buckets]
            except KeyError:
                pass
    z_percentile = (np.argsort(np.argsort(z.flat)) / z.max()).reshape(z.shape)  # Percentile version
    # z.clip(max=2, out=z)
    x = num_elementss
    y = num_bucketss
    fig, ax = plt.subplots()
    ax.set_title(f"approx_ops / num_elements ({title})")
    ax.set_xlabel("num_elements")
    ax.set_ylabel("num_buckets")
    b = sorted(z.flat)
    # b = [x for x in b if x < 16]
    b = [b[(len(b) - 1) * i // 256] for i in range(256 + 1)]
    bounds = np.array(b)
    norm = colors.BoundaryNorm(boundaries=bounds, clip=True, ncolors=len(bounds))
    pcm = ax.pcolormesh(x, y, z, norm=norm)
    fig.colorbar(pcm, ax=ax, extend="max", orientation="vertical")
    y = np.array([min(approx_ops[no], key=lambda nb: approx_ops[no][nb]) for no in x])
    print("Optimal num_buckets / num_elements ratio:", y / x)
    plt.plot(x, y, 'r:')
    # plt.plot([min(x), max(x)], [min(y), max(y)], "r:")
    plt.grid()
    plt.savefig(out_filename, dpi=600)


approx_ops_base_2, approx_ops_base_e = load_approx_ops_csv("output_v5.csv")
plot(approx_ops_base_2, "approx_ops_base_2_v5.png", "Base 2")
plot(approx_ops_base_e, "approx_ops_base_e_v5.png", "Base e")
