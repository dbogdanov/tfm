#Script1_Images

import scipy
import numpy as np
import matplotlib.pyplot as plt
import glob
import csv
import pandas as pd
import seaborn as sns
import os


def get_files_in_dir(dirname, extension):
    return glob.glob(os.path.join(dirname, "*/*.%s" % extension))


def main():
	directory = input("Write the directory to use as data\n")
	print "The data directory is " + directory

	extension = input("Write the extension of the files to use\n")
	print "Collecting data with format ." + extension

	ListOfFiles = get_files_in_dir(directory,extension)
	print ListOfFiles
	return(ListOfFiles)
'''
	with open("./testDB/last_fm.csv", "rb") as f:
		line=[line.split() for line in f]  

    	CorList = []

    	for i in range (0,6301):
        	CorLine = []
        	CorLine.append(str(line[i]).split(','))
        	CorList.append(str(CorLine[0]).split(','))

	AsianList = []
	BluesList = []
	ClassicalList = []
	ClatinamerList = []
	CountryList = []
	EasyList = []
	ElectronicList = []
	FolkList = []
	HiphopList = []
	JazzList = []
	PopList = []
	RnbList = []
	RockList = []
	SkaList = []


	for i in range(1,len(CorList)):
	    if str(CorList[i][1]).split("'")[1] == 'asian':
		for j in range (2,270):
		    AsianList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'blues':
		for j in range (2,270):
		    BluesList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'classical':
		for j in range (2,270):
		    ClassicalList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'clatinamer':
		for j in range (2,270):
		    ClatinamerList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'country':
		for j in range (2,270):
		    CountryList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'easylistening':
		for j in range (2,270):
		    EasyList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'electronic':
		for j in range (2,270):
		    ElectronicList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'folk':
		for j in range (2,270):
		    FolkList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'hiphop':
		for j in range (2,270):
		    HiphopList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'jazz':
		for j in range (2,270):
		    JazzList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'pop':
		for j in range (2,270):
		    PopList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'rnb':
		for j in range (2,270):
		    RnbList.append(CorList[i][j][2:len(CorList[i][j])-1])
		    
	    if str(CorList[i][1]).split("'")[1] == 'rock':
		for j in range (2,270):
		    RockList.append(CorList[i][j][2:len(CorList[i][j])-1])
	    
	    if str(CorList[i][1]).split("'")[1] == 'ska':
		for j in range (2,270):
		    SkaList.append(CorList[i][j][2:len(CorList[i][j])-1])


	Asian = np.zeros([450,268])  #change 450  by len(AsianList)
	Blues = np.zeros([450,268])
	Classical = np.zeros([450,268])
	Clatinamer = np.zeros([450,268])
	Country =  np.zeros([450,268])
	Easy = np.zeros([450,268])
	Electronic = np.zeros([450,268])
	Folk = np.zeros([450,268])
	Hiphop = np.zeros([450,268])
	Jazz = np.zeros([450,268])
	Pop = np.zeros([450,268])
	Rnb = np.zeros([450,268])
	Rock = np.zeros([450,268])
	Ska = np.zeros([450,268])

	k = 0
	for i in range (0,450):
	    for j in range (0,268):
		Asian[i][j] = AsianList[k]
		Blues[i][j] = BluesList[k]
		Classical[i][j] = ClassicalList[k]
		Clatinamer[i][j] = ClatinamerList[k]
		Country[i][j] = CountryList[k]
		Easy[i][j] = EasyList[k]
		Electronic[i][j] = ElectronicList[k]
		Folk[i][j] = FolkList[k]
		Hiphop[i][j] = HiphopList[k]
		Jazz[i][j] = JazzList[k]
		Pop[i][j] = PopList[k]
		Rnb[i][j] = RnbList[k]
		Rock[i][j] = RockList[k]
		Ska[i][j] = SkaList[k]
		k = k+1

	FeatAsian = np.zeros(len(Asian))
	FeatBlues = np.zeros(len(Blues))
	FeatClassical = np.zeros(len(Classical))
	FeatClatinamer = np.zeros(len(Clatinamer))
	FeatCountry = np.zeros(len(Country))
	FeatEasy = np.zeros(len(Easy))
	FeatElectronic = np.zeros(len(Electronic))
	FeatFolk = np.zeros(len(Folk))
	FeatHiphop = np.zeros(len(Hiphop))
	FeatJazz = np.zeros(len(Jazz))
	FeatPop = np.zeros(len(Pop))
	FeatRnb = np.zeros(len(Rnb))
	FeatRock = np.zeros(len(Rock))
	FeatSka = np.zeros(len(Ska))


	def namestr(obj, namespace):
	    return [name for name in namespace if namespace[name] is obj]

	for numFeat in [4,266]:
	    for i in range(0,len(FeatAsian)):
		FeatAsian[i] = Asian[i][numFeat]
		FeatBlues[i] = Blues[i][numFeat]
		FeatClassical[i] = Classical[i][numFeat]    
		FeatClatinamer[i] = Clatinamer[i][numFeat]   
		FeatCountry[i] = Country[i][numFeat]
		FeatEasy[i] = Easy[i][numFeat]
		FeatElectronic[i] = Electronic[i][numFeat]
		FeatFolk[i] = Folk[i][numFeat]
		FeatHiphop[i] = Hiphop[i][numFeat]
		FeatJazz[i] = Jazz[i][numFeat]
		FeatPop[i] = Pop[i][numFeat]
		FeatRnb[i] = Rnb[i][numFeat]
		FeatRock[i] = Rock[i][numFeat]
		FeatSka[i] = Ska[i][numFeat]
	
	    sns.distplot(FeatAsian) #b
	    sns.distplot(FeatBlues) #g
	    sns.distplot(FeatClassical) #r
	    sns.distplot(FeatClatinamer) #p
	    sns.distplot(FeatCountry) #y
	    sns.distplot(FeatEasy) #c
	    sns.distplot(FeatElectronic) #b
	    sns.distplot(FeatFolk) #g
	    sns.distplot(FeatHiphop) #r
	    sns.distplot(FeatJazz) #p
	    sns.distplot(FeatPop) #y
	    sns.distplot(FeatRnb) #c
	    sns.distplot(FeatRock) #b
	    sns.distplot(FeatSka) #g
	    os.makedirs('IMAGESS')
	    s = "%s_all.png" %str(CorList[0][numFeat])[11:]
	    s = os.path.join("/home/pedro/TFM/IMAGESS", s)
	    #plt.savefig('%s.png' % s)
	    plt.savefig(s)
	    plt.clf()
	    
	    for genre1 in [FeatAsian,FeatBlues,FeatClassical,FeatClatinamer,FeatCountry,FeatEasy,FeatElectronic,FeatFolk,FeatHiphop,FeatJazz,FeatPop,FeatRnb,FeatRock,FeatSka]:
		for genre2 in [FeatAsian,FeatBlues,FeatClassical,FeatClatinamer,FeatCountry,FeatEasy,FeatElectronic,FeatFolk,FeatHiphop,FeatJazz,FeatPop,FeatRnb,FeatRock,FeatSka]:
		    sns.distplot(genre1)
		    sns.distplot(genre2)
		    s = "%(t)s_%(x)s_%(y)s.png" % {"t" : str(CorList[0][numFeat])[11:] , "x" : namestr(genre1,globals())[0][4:], "y" : namestr(genre2,globals())[0][4:]}
		    s = os.path.join("/home/pedro/TFM/IMAGESS", s)
		    #plt.savefig('%s.png' % s)
		    plt.savefig(s)
		    plt.clf()
'''
#	return()

main()
