#Script1_Images

import numpy as np
import matplotlib.pyplot as plt
import glob
import csv
import seaborn
import os
import math
from scipy import stats
from operator import itemgetter
import codecs
import json


def namestr(obj, namespace):
    	return [name for name in namespace if namespace[name] is obj]

def get_files_in_dir(dirname, extension):
    	return glob.glob(os.path.join(dirname, "*/*.%s" % extension))


def main():

	#USE SYS.ARGV
	directory = input("Write the directory to use as data\n")
	print "The data directory is " + directory

	extension = input("Write the extension of the files to use (json recommended)\n")
	print "Collecting data with format ." + extension

	result_dir = input("Write a name for the results folder\n")
	print "The results directory is " + result_dir

	os.makedirs(result_dir)

	ListOfFiles = get_files_in_dir(directory,extension)	

#Convert to csv file to have all the data in the same file


	#SHOULD USE THE JSON_TO_CSV IMPORTED AND NOT AS SHELL (/*/*.json)
	os.system("python json_to_csv.py -i " + str(ListOfFiles).translate(None, '[],\'') +  " -o " + result_dir + "/DataSet.csv --include metadata.audio_properties.* metadata.tags.musicbrainz_recordingid.0 lowlevel.* rhythm.* tonal.* --ignore *.min *.min.* *.max *.max.* *.dvar *.dvar2 *.dvar.* *.dvar2.* *.dmean *.dmean2 *.dmean.* *.dmean2.* *.cov.* *.icov.* rhythm.beats_position.* --add-filename")
	


	#LOADING DATA FROM CSV TO DICT

	DICT = {}
	reader = csv.DictReader(open(result_dir + '/DataSet.csv'))
	genre = []

	for row in reader:
	    	genre.append(str(os.path.dirname(row['json_file_name'])).split("/")[-1])
	genre = set(genre)

	reader = csv.DictReader(open(result_dir + '/DataSet.csv'))
	for row in reader:
	   	for column, value in row.items():
			DICT.setdefault(column, []).append(value)

	numKey = 0
	reader = csv.DictReader(open(result_dir + '/DataSet.csv'))
	for key in DICT:
		numKey = numKey + 1
    		DICT[key] = {}
		for g in genre:
			DICT[key][g] = []
	reader = csv.DictReader(open(result_dir + '/DataSet.csv'))
	for row in reader:
    		for g in genre:
        		if str(os.path.dirname(row['json_file_name'])).split("/")[-1] == g:
            			for key in DICT:
					try:
						DICT[key][g].append(row[key])
					except:
						None

	pValues = np.zeros((len(genre)*len(genre)*numKey),dtype=[('baz', '|S10'),('bay', '|S10'),('baw', '|S25'),('foo', '>f4'), ('bar', '>f4') ])
	FAILS = 0
	j = 0
	for key in DICT:
    		if key != 'json_file_name':
			try:
				for g in genre:
		    			feat1 = np.zeros(len(DICT[key][g]))
		    			for i in range(0,len(DICT[key][g])):
		        			feat1[i] = DICT[key][g][i]
		        			#feat1[i] = str(DICT[key][g][1]).split("'")[1]
		    			seaborn.distplot(feat1)
	       			#plt.show()
				s = "%s_all.png" %key
				s = os.path.join("%s" %result_dir, s)
				plt.savefig(s)
				plt.clf()
			except:
				print("\n Couldn't plot the feature %s" % key)
				FAILS = FAILS +1
        
			
        		for g in genre:
            			for h in genre:
					try:
		        			feat2 = np.zeros(len(DICT[key][h]))
		      				feat1 = np.zeros(len(DICT[key][g]))
		        			for i in range(0,len(DICT[key][g])):
		            				feat1[i] = DICT[key][g][i]
							feat2[i] = DICT[key][h][i]
		            				#feat1[i] = str(DICT[key][g][i]).split("'")[1]
		            				#feat2[i] = str(DICT[key][h][i]).split("'")[1]
		        			seaborn.distplot(feat1)
		       				seaborn.distplot(feat2)
		        			s = "%(t)s_%(x)s_%(y)s.png" % {"t" : key, "x" : g, "y": h}
		        			s = os.path.join("%s" %result_dir, s)
		        			plt.savefig('%s.png' % s)
		        			plt.clf()
					except:
						print("-")

	

					
					pValues[j][0] = g
					pValues[j][1] = h
					pValues[j][2] = key
					pValues[j][3] = stats.ks_2samp(DICT[key][g],DICT[key][h])[0] #KS_Statistic
					pValues[j][4] = stats.ks_2samp(DICT[key][g],DICT[key][h])[1] #twoTailed_pValue
					j = j+1

	print("The number of non-plotted features is: " + str(FAILS))

	print ("---------------------\nAll the images have been saved in %s \n&\nThe KolmogorovTest has been computed\n---------------------\n" % dir)


	from operator import itemgetter
	OrdPValues = np.zeros((len(genre)*len(genre)*numKey),dtype=[('baz', '|S10'),('bay', '|S10'),('baw', '|S25'),('foo', '>f4'), ('bar', '>f4') ])

	pVal = pValues.tolist() #to make it jsonizable
	OrdPValues = sorted(pVal,key=itemgetter(4))

	Kolmogorov_path = result_dir + "/KolTest.json"

	print("The Kolmogorov Test has been saved in the output folder")

	json.dump(OrdPValues, codecs.open(Kolmogorov_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

	return()


main()
