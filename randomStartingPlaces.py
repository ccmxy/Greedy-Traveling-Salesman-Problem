################################################
######## Travelling Salesman Solution: #########
### RANDOM STARTING CITY + NEAREST CITY~~ ######
# A slightly better, though 40x slower, solution
# to the travelling salseman problem as compared
# to simpleGreedy.py. This time 40 starting
# cities are chosen at random, and the one that
# leads to the shortest 'nearest city next' greedy
# path is kept.
#            By Colleen Minor.
################################################

import sys
import argparse
import math
import random
import copy

#Specify command line arguments with argsparse
parser = argparse.ArgumentParser(
    description='''Description of our program goes here, and we can include
         a more detailed description or whatever maybe for when they hit -h
             if that's a thing we want to do''')
parser.add_argument('inputFile', metavar='inputFile',
     help='This is file containing a list of (cityNumber, X-coordinate, Y-coordinate).')

#Function to return an array of arrays of
#each line in the file.
def loadArrayOfArraysFromFile(fileName):
        lines = []
        with open(fileName) as file:
                for line in file:
                    line = map(int, line.split())
                    lines.append(line)
                return lines

#this returns distance_matrix, an
# array of arrays of the distances from
# each city to each other city.
def getDistanceMatrix(cities):
    distanceMatrix = []
    for currentNode in cities:
        subArray = []
        for comparisonNode in cities:
            subArray.append(getDistanceBetweenTwoCities(currentNode, comparisonNode))
        distanceMatrix.append(subArray)
    return distanceMatrix


#city1 and city2 are both arrays like, [id, X-coordinate, Y-coordinate]
def getDistanceBetweenTwoCities(city1, city2):
    x1 = city1[1]
    y1 = city1[2]
    x2 = city2[1]
    y2 = city2[2]
    numToGetSquareRootOf = ((pow((x1 - x2), 2)) + (pow((y1 - y2), 2)))
    if numToGetSquareRootOf < 0:
        numToGetSquareRootOf *= -1
    return int(round(math.sqrt(numToGetSquareRootOf)))


################################################
############### getNearestCity #################
# Returns the closest city to city with id cityID
################################################
################################################
def getNearestCity(distanceMatrix, cityId):
    i = 0
    for distanceList in distanceMatrix:
        if i == cityId:
            smallestDistance = min(idx for idx in distanceList if idx > 0)
            if smallestDistance > 9999 * 3:
                return -1, -1
            else:
                return smallestDistance, distanceList.index(smallestDistance)
        i += 1

################################################
########## getDistanceForTripHome ##############
#Return the distane between the first and last
# cities in the path
################################################
################################################
def getDistanceForTripHome(thePath, cities):
    for city in cities:
        if city[0] == thePath[0]: #If first city in path
            firstCity = city
        if city[0] == thePath[len(thePath) - 1]: #If last city in path
            lastCity = city
    return getDistanceBetweenTwoCities(firstCity, lastCity)

################################################
################## addCity ##################
# Adds city to pathArray and removes it from citiesToVisit.
# Modifies: pathArray, citiesToVisit, distanceList
################################################
################################################
def addCity(pathArray, citiesToVisit, distanceMatrix, city_id):
    pathArray.append(city_id)
    prev_city_id = pathArray[len(pathArray) - 2]
    for city in citiesToVisit:
        if city[0] == prev_city_id:
            citiesToVisit.remove(city)

    for distanceList in distanceMatrix:
        distanceList[prev_city_id] = 99999


################################################
################## chooseCity ##################
#Return success flag, id of the city with the best distance between
# the middle 2 cities in citiesToVisit, and midIndex_2
################################################
################################################
def chooseCity(pathArray, citiesToVisit, distanceMatrix):
    if len(pathArray) == 0: #If path empty, return starting node
        randomStartingCity = random.randint(0, (len(distanceMatrix) - 1))
        return 0, randomStartingCity, 0
    bestDistance, idOfBestCity = getNearestCity(distanceMatrix, pathArray[(len(pathArray) - 1)])
    if idOfBestCity == -1:
        return  -1, -1, -1 #Indicates we are done visiting cities
    return 0, idOfBestCity, bestDistance

################################################
############### findGreedyRandomPath ###########
# Returns a greedy random path
################################################
################################################
def findGreedyRandomPath(cities):
    pathArray = [] #array to hold the paths that we will use
    flag = 0 #Holds flag as to weather we are done adding cities
    totalDistance = 0 #Holds the total distance (in theory)
    distance_matrix = getDistanceMatrix(cities) #returns a matrix of city distances

    cities_to_add = copy.deepcopy(cities)
    distanceMatrix = copy.deepcopy(distance_matrix)
    #Add cities until we have added them all.
    while flag is not -1:
        flag, city_id, distance = chooseCity(pathArray, cities_to_add, distanceMatrix)
        if flag == 0:
            addCity(pathArray, cities_to_add, distanceMatrix, city_id)
            totalDistance += distance

    return totalDistance, pathArray #Return the final path

################################################
############### bestRandStart ###################
# Return the shortest path found out of 40 greedy
# paths (nearest city prioritized) with randomly
# chosen starting cities.
################################################
################################################
def bestRandStart(cities):
    bestPath = []
    distance_matrix_copy = []
    lowestDistance = 99999999
    for i in range(0, 40):
        pathDistance, thePath = findGreedyRandomPath(cities)
        pathDistance += getDistanceForTripHome(thePath, cities)
        if pathDistance < lowestDistance:
            lowestDistance = copy.deepcopy(pathDistance)
            bestPath = thePath
    return lowestDistance, bestPath

#main
if __name__ == "__main__":

    args = parser.parse_args()
    inputFile = (args.inputFile)

    cities = loadArrayOfArraysFromFile(inputFile) #get 2d array of int arrays of cities
    distance_matrix = getDistanceMatrix(cities) #returns a matrix of city distances

    #Retreive the total distance travelled and the path
    totalDistance, thePath = bestRandStart(cities)

    #Write to output file
    outFile = open(inputFile + ".tour", 'w')
    print>>outFile, totalDistance
    for node in thePath:
        print>>outFile, node
