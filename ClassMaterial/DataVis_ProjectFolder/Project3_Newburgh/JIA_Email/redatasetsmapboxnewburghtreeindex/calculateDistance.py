#calculateDistance

import csv
import json
import collections
import operator
from pprint import pprint
 
treeFilePath = 'newburgh_trees.geojson'
treeData=open(treeFilePath)
trees = json.load(treeData)

siteFilePath = "DEC Map - Sheet1.csv"
siteData = open(siteFilePath)
sites = csv.reader(siteData)
next(sites, None)
 
#calculate distance between 2 points or 2 coordinate pairs	
#in miles
def calculateDistance(lat1,lng1,lat2,lng2):
	from math import sin, cos, sqrt, atan2, radians
	R = 3958.8

	lat1 = radians(lat1)
	lng1 = radians(lng1)
	lat2 = radians(lat2)
	lng2 = radians(lng2)

	dlng = lng2 - lng1
	dlat = lat2 - lat1
	a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlng/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c
	return distance

outputfile = open("trees_distances_nearestSite.geojson", "w")

newTrees = {}
newTrees["crs"]=trees["crs"]
newTrees["type"]=trees["type"]
newTrees["features"]=[]
#make a list of coordinate pairs, 2 points each for each tree to site
for tree in trees["features"]:
    siteData.seek(0)
    next(sites, None)
    tlat = float(tree["geometry"]["coordinates"][1])
    tlng = float(tree["geometry"]["coordinates"][0])
    minDistance =100000
    nearestSite = "NA"
    for site in sites:
        slat = float(site[2])
        slng = float(site[3])
        distance = calculateDistance(tlat,tlng,slat,slng)
        #print distance
        if distance<minDistance:
            nearestSite = site[0]
            minDistance = distance

            tree["properties"]["nearestSite"]=nearestSite
            tree["properties"]["minDistance"]=minDistance
    print minDistance,nearestSite
         
    #print tree["properties"]["minDistance"]
    #print tree["properties"]["nearestSite"]
    newTrees["features"].append(tree)
    
json.dump(newTrees,outputfile)