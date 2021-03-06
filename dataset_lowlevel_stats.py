import os
import glob
import json
import csv
from argparse import ArgumentParser
from json_to_csv import parse_descriptors
import itertools
import seaborn
import matplotlib.pyplot as plt
import operator

import numpy as np
from scipy import stats


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def get_files_in_dir(dirname, extension):
    return glob.glob(os.path.join(dirname, "*/*.%s" % extension))

def process_all(input_dir, results_dir, include, ignore, only_interesting, overall):

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Load dataset
    data = {}
    json_files = get_files_in_dir(input_dir, 'json')
    for f in json_files:
        path, filename = os.path.split(f)
        path = os.path.split(path)
        if len(path) == 2:
            category = path[-1]
        else:
            print "Skipping", f
            continue

        recording = json.load(open(f, 'r'))
        recording_normalized = parse_descriptors(recording, include, ignore)

        for feature, value in recording_normalized.items():
            data.setdefault(feature, {})
            data[feature].setdefault(category, [])
            data[feature][category].append(value)

    ks = []
    for feature in data.keys():
        pairs = list(itertools.combinations(data[feature].keys(), 2))
        for g1, g2 in pairs:
            # Kolmogorov-Smirnov test (KS_Statistic, twoTailed_pValue)
            st, p = stats.ks_2samp(np.array(data[feature][g1]), np.array(data[feature][g2]))
            ks.append([feature, g1, g2, st, p])

    with open(os.path.join(results_dir, 'stats.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for row in ks:
            writer.writerow(row)

    ks_sorted = sorted(ks, key=operator.itemgetter(4))

    with open(os.path.join(results_dir, 'stats_sorted.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for row in ks_sorted:
            writer.writerow(row)

    if overall:
        # Overall distribution plots (all categories)
        for feature in data.keys():
            try:
                for category in data[feature].keys():
                    seaborn.distplot(data[feature][category], kde_kws={"label": category})
                plt.savefig(os.path.join(results_dir, feature + '.png'))
                plt.clf()

            except:
                print "Error plotting", feature

    if only_interesting:
        ks_sorted = [(feature, g1, g2, ks, p_value) for feature, g1, g2, ks, p_value in ks_sorted if p_value <= 0.05]
        ks_sorted = sorted(ks_sorted)

    html = ''
    for feature, g1, g2, ks, p_value in ks_sorted:
        try:
            seaborn.distplot(data[feature][g1], axlabel=feature + ' (p=%.2f)' % p_value, kde_kws={"label": g1})
            seaborn.distplot(data[feature][g2], kde_kws={"label": g2})
            plot_file = os.path.join(results_dir, feature + '-' + g1 + '-' + g2 + '.png')
            plt.savefig(plot_file)
            plt.clf()
            html += '<div><p>%s | %s - %s (p=%.2f)</p><img src="%s"></div>' % (feature, g1, g2, p_value, plot_file)
        except:
            print "Error plotting", feature

    with open(os.path.join(results_dir, 'stats_plots.html'), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    parser = ArgumentParser(description = """
Provides statistics for low-level features distribution per class in a dataset.
""")
    parser.add_argument('-i', '--input_dir', help='Input directory with descriptor json files', required=True)
    parser.add_argument('-o', '--results_dir', help='Output directory to write results', required=True)
    parser.add_argument('--include', nargs='+', help='Descriptors to include (can use wildcards)', required=False)
    parser.add_argument('--ignore', nargs='+', help='Descriptors to ignore (can use wildcards)', required=False)
    parser.add_argument('--only-interesting', dest='only_interesting', help='Plot only interesting results', action='store_true')
    parser.add_argument('--plot-overall', dest = 'overall', help='Plot overall plot (all categories)', action='store_true')

    args = parser.parse_args()

    if args.include and args.ignore and not set(args.include).isdisjoint(args.ignore):
        print 'You cannot specify the same descriptor patterns in both --include and --ignore flags'
        sys.exit()

    process_all(args.input_dir, args.results_dir, args.include, args.ignore, args.only_interesting, args.overall)