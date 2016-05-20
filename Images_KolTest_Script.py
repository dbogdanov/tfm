#Script1_Images

import scipy
import numpy as np
import matplotlib.pyplot as plt
import glob
import csv
import pandas as pd
import seaborn as sns
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
	directory = input("Write the directory to use as data\n")
	print "The data directory is " + directory

	extension = input("Write the extension of the files to use (json recommended)\n")
	print "Collecting data with format ." + extension

	ListOfFiles = get_files_in_dir(directory,extension)	

#Convert to csv file to have all the data in the same file

	os.system("python json_to_csv.py -i " + str(ListOfFiles).translate(None, '[],\'') +  " -o DataSet.csv --include metadata.audio_properties.* metadata.tags.musicbrainz_recordingid.0 lowlevel.* rhythm.* tonal.* --ignore *.min *.min.* *.max *.max.* *.dvar *.dvar2 *.dvar.* *.dvar2.* *.dmean *.dmean2 *.dmean.* *.dmean2.* *.cov.* *.icov.* rhythm.beats_position.* --add-filename")
	

	with open("./DataSet.csv", "rb") as f:
		line=[line.split() for line in f]  

    	CorList = []

#Collect all the data from the created csv

    	for i in range (0,len(line)):
        	CorLine = []
        	CorLine.append(str(line[i]).split(','))
        	CorList.append(str(CorLine[0]).split(','))

	CorList[0].append("Genre")
	for i in range(1,len(CorList)):
		CorList[i].append(str(CorList[i][0]).split('/')[-2])
		
	Genres = []
	for i in range(1,len(CorList)):
		Genres.append(CorList[i][-1])

	Genres = sorted(set(Genres))
	NumGenres = len(Genres)


#Create a list for each genre (only used to created the Matrices of the genres)

	for i in range(0, len(Genres)):
   		globals()['genre%s' % i] = []


	for i in range(1,len(CorList)):
	    	for x in range(0,len(Genres)):
			if str(CorList[i][-1]) == Genres[x]:
		    		for j in range (0,len(CorList[i])):
		        		globals()['genre%s' % x].append(CorList[i][j][0:len(CorList[i][j])-1])

#Create a Matrix for each genre splitting the list, where rows are different json files and columns are different features

	for i in range(0,len(Genres)):
    		globals()['genreMat%s' % i]=np.zeros([math.ceil(len(globals()['genre%s' % i])/float(len(CorList[i]))),len(CorList[i])-1])




	for x in range(0,len(Genres)):
    		k = 0
    		for i in range (0,len(globals()['genreMat%s' % x])):
        		for j in range (0,len(globals()['genreMat%s' % x][i])):
            			try:
                			globals()['genreMat%s' % x][i][j] = str(globals()['genre%s' % x][k]).split("'")[1]
            			except:
                			globals()['genreMat%s' % x][i][j] = 0
            			k = k+1



	for x in range(0, len(Genres)):
    		globals()['featGenre%s' % x] = np.zeros(len(globals()['genreMat%s' % x]))
	
#Create a new folder to save the images to avoid errors if the folder exists
	x = 1
	while (x != 0):
    		try:
        		os.makedirs('IMAGES%d' %x)
        		dir = 'IMAGES%d' %x
        		x = 0
        		break
    		except:
        		x = x+1

#For the desired features, plot in an image the distribution of the variables in order to compare among genres their distributions
	pValues = np.zeros((len(Genres)*len(Genres)*(len(CorList)-1)),dtype=[('baz', '|S10'),('bay', '|S10'),('baw', '|S25'),('foo', '>f4'), ('bar', '>f4') ])


#Now is with all the Features, but it seems to break in my laptop when there are too many features. Change the numFeat number of iterations if needed.
	for numFeat in range(1,len(CorList[0])): 
    		for x in range(0,len(Genres)):
        		for i in range(0,len(globals()['featGenre%s' % x])):
            			globals()['featGenre%s' % x][i] = globals()['genreMat%s' % x][i][numFeat]
        		for i in range(0,len(globals()['featGenre%s' % x])):
            			sns.distplot(globals()['featGenre%s' % x])

        		s = "%s_all.png" %str(CorList[0][numFeat])[12:-2]
			s = os.path.join("/home/pedro/TFM/%s" %dir, s)
			#plt.savefig('%s.png' % s)
			plt.savefig(s)
			plt.clf()

		j = 0
		for genre1 in range(0,len(Genres)):
		    for genre2 in range(0,len(Genres)):
			sns.distplot(globals()['featGenre%s' % genre1])
			sns.distplot(globals()['featGenre%s' % genre2])

			s = "%(t)s_%(x)s_%(y)s.png" % {"t" : str(CorList[0][numFeat])[12:-2] , "x" : Genres[int(namestr(globals()['featGenre%s' %genre1],globals())[0][9:])], "y" : Genres[int(namestr(globals()['featGenre%s' %genre2],globals())[0][9:])]}
#Saving images
			s = os.path.join("/home/pedro/TFM/%s" %dir, s)
			plt.savefig('%s.png' % s)
			plt.clf()

#KOLMOGOROV TEST

			pValues[j][3] = stats.ks_2samp(namestr(globals()['featGenre%s' %genre1],globals()),namestr(globals()['featGenre%s' %genre2],globals())
)[0] #KS_Statistic
        		pValues[j][4] = stats.ks_2samp(namestr(globals()['featGenre%s' %genre1],globals()),namestr(globals()['featGenre%s' %genre2],globals())
)[1] #twoTailed_pValue
        		pValues[j][0] = Genres[int(namestr(globals()['featGenre%s' %genre1],globals())[0][9:])]
        		pValues[j][1] = Genres[int(namestr(globals()['featGenre%s' %genre2],globals())[0][9:])]
			pValues[j][2] = str(CorList[0][numFeat])[11:]
			j = j+1


	print ("---------------------\nAll the images have been saved in %s \n&\nThe KolmogorovTest has been computed\n---------------------\n" % dir)


	from operator import itemgetter
	OrdPValues = np.zeros((len(Genres)*len(Genres)*(len(CorList)-1)),dtype=[('baz', '|S10'),('bay', '|S10'),('baw', '|S25'),('foo', '>f4'), ('bar', '>f4') ])

	pVal = pValues.tolist() #to make it jsonizable
	OrdPValues = sorted(pVal,key=itemgetter(4))

	Kolmogorov_path = input("Write the directory of the json file to save the Kolmogorov Test data\n(it needs the .json extension)\n")

	json.dump(OrdPValues, codecs.open(Kolmogorov_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

	return()


main()
