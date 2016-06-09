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

def process_all(input_dir, results_dir, include, ignore):

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
        # Overall distribution plots
        try:
            for category in data[feature].keys():
                #print feature, category, type(data[feature][category]), len(data[feature][category])
                seaborn.distplot(data[feature][category])
            plt.savefig(os.path.join(results_dir, feature + '.png'))
            plt.clf()

        except:
            print "Error plotting", feature

        # Pairwise distribution plots
        pairs = list(itertools.combinations(data[feature].keys(), 2))
        for g1, g2 in pairs:
            try:
                seaborn.distplot(data[feature][g1])
                seaborn.distplot(data[feature][g2])
                plt.savefig(os.path.join(results_dir, feature + '-' + g1 + '-' + g2 + '.png'))
                plt.clf()
            except:
                print "Error plotting", feature

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


if __name__ == '__main__':
    parser = ArgumentParser(description = """
Provides statistics for low-level features distribution per class in a dataset. 
""")
    parser.add_argument('-i', '--input_dir', help='Input directory with descriptor json files', required=True)
    parser.add_argument('-o', '--results_dir', help='Output directory to write results', required=True)
    parser.add_argument('--include', nargs='+', help='Descriptors to include (can use wildcards)', required=False)
    parser.add_argument('--ignore', nargs='+', help='Descriptors to ignore (can use wildcards)', required=False)
    args = parser.parse_args()

    if args.include and args.ignore and not set(args.include).isdisjoint(args.ignore):
        print 'You cannot specify the same descriptor patterns in both --include and --ignore flags'
        sys.exit()

    process_all(args.input_dir, args.results_dir, args.include, args.ignore)


"""
    from operator import itemgetter
	OrdPValues = np.zeros((len(genre)*len(genre)*numKey),dtype=[('baz', '|S10'),('bay', '|S10'),('baw', '|S25'),('foo', '>f4'), ('bar', '>f4') ])

	pVal = pValues.tolist() #to make it jsonizable
	OrdPValues = sorted(pVal,key=itemgetter(4))

	Kolmogorov_path = result_dir + "/KolTest.json"

	print("The Kolmogorov Test has been saved in the output folder")

	json.dump(OrdPValues, codecs.open(Kolmogorov_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

	return()


main()
"""