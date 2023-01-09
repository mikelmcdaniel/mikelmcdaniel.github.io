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
    with open(csv_filename, "r") as f:
        for row in csv.DictReader(f):
            num_elements = int(row["num_elements"])
            num_buckets = int(row["num_buckets"])
            if num_buckets < 2:
                continue
            approx_ops_base_2[num_elements][num_buckets] = (
                float(row["approx_ops_base_2"]) / num_elements
            )
            approx_ops_base_e[num_elements][num_buckets] = (
                float(row["approx_ops_base_e"]) / num_elements
            )
    return approx_ops_base_2, approx_ops_base_e


def plot(approx_ops, out_filename, sub_title=""):
    num_elementss = sorted(num_elements for num_elements in approx_ops)
    num_bucketss = sorted(
        set(num_buckets for sub_dict in approx_ops.values() for num_buckets in sub_dict)
    )
    width = len(num_elementss)
    height = len(num_bucketss)

    z = np.zeros((height, width))
    for x, num_elements in enumerate(num_elementss):
        for y, num_buckets in enumerate(num_bucketss):
            z[y, x] = approx_ops[num_elements][num_buckets]
    x = num_elementss
    y = num_bucketss
    fig, ax = plt.subplots()
    # ax.set_title(f"approx_ops / num_elements ({sub_title}) (min={z.min():.4f})")
    # ax.set_xlabel("num_elements")
    # ax.set_ylabel("num_buckets")
    ax.set_title(f"O(f(N, B)) / N (min={z.min():.4f})")
    ax.set_xlabel("N  (number of elements)")
    ax.set_ylabel("B  (number of buckets)")

    sorted_z = sorted(z.flat)
    boundaries = [sorted_z[(len(sorted_z) - 1) * i // 256] for i in range(256 + 1)]
    norm = colors.BoundaryNorm(
        boundaries=boundaries, clip=True, ncolors=len(boundaries)
    )
    pcm = ax.pcolormesh(x, y, z, norm=norm)
    fig.colorbar(pcm, ax=ax, extend="max", orientation="vertical")

    y = np.array([min(approx_ops[no], key=lambda nb: approx_ops[no][nb]) for no in x])
    print("Optimal num_buckets / num_elements ratio:", y / x)
    plt.plot(x, y, "r:")

    plt.grid()
    plt.savefig(out_filename, dpi=600)


approx_ops_base_2, approx_ops_base_e = load_approx_ops_csv("output_v5.csv")
plot(approx_ops_base_2, "approx_ops_base_2_v5.png", "Base 2")
plot(approx_ops_base_e, "approx_ops_base_e_v5.png", "Base e")
approx_ops_base_2, approx_ops_base_e = load_approx_ops_csv("output_v7.csv")
plot(approx_ops_base_2, "approx_ops_base_2_v7.png", "Base 2")
plot(approx_ops_base_e, "approx_ops_base_e_v7.png", "Base e")
