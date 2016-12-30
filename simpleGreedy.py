################################################
######## Travelling Salesman Solution: #########
### NEAREST CITY~~ A SIMPLE GREEDY ALGORITHM ###
# A simple solution to the travelling Salesman
# problem.
#           By Colleen Minor.
################################################

import sys
import argparse
import math

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

#this returns distanceMatrix, an
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
############### getNeighborCities ##############
# Returns the closest two cities in distanceMatrix
################################################
################################################
def getNeighborCities(distanceMatrix):
    closeCity_1 = 0
    closeCity_2 = -1
    smallestDistance = 99999
    for distanceList in distanceMatrix:
        temp = min(i for i in distanceList if i > 0)
        if temp < smallestDistance:
            smallestDistance = temp
            closeCity_1 = distanceList.index(smallestDistance)
            closeCity_2 = distanceMatrix.index(distanceList)
    return closeCity_1, closeCity_2

################################################
############### bestBetweenCities ##############
# Finds the best city between two cities, given
# arrays of each of their distances to other cities.
# This is the only one I don't actually use in this
# program, but leaving here for future reference in
# case someone would want to uses this for a different
# algorithm.
################################################
################################################
def bestBetweenCities(distArray_1, distArray_2):
    minDist = 99999 * 2
    minIndex = -1
    for i in range(0, len(distArray_1)):
        fromBoth = distArray_1[i] + distArray_2[i]
        if fromBoth < minDist:
            minDist = fromBoth
            minIndex = i
    return minDist, minIndex


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
        return 0, 0, 0

    bestDistance, idOfBestCity = getNearestCity(distanceMatrix, pathArray[(len(pathArray) - 1)])

    if idOfBestCity == -1:
        return  -1, -1, -1 #Indicates we are done visiting cities

    return 0, idOfBestCity, bestDistance

################################################
############### findBestPath ###################
# Returns the best path
################################################
################################################
def findBestPath(distanceMatrix, cities_to_add):
    #startingCity, endingCity = getNeighborCities(distanceMatrix)
    pathArray = [] #array to hold the paths that we will use
    flag = 0 #Holds flag as to weather we are done adding cities
    totalDistance = 0 #Holds the total distance (in theory)

    #Add cities until we have added them all.
    while flag is not -1:
        flag, city_id, distance = chooseCity(pathArray, cities_copy, distanceMatrix)
        if flag == 0:
            addCity(pathArray, cities_to_add, distanceMatrix, city_id)
            totalDistance += distance

    return totalDistance, pathArray #Return the final path to main


#main
if __name__ == "__main__":

    args = parser.parse_args()
    inputFile = (args.inputFile)

    cities = loadArrayOfArraysFromFile(inputFile) #get 2d array of int arrays of cities
    cities_copy = list(cities) #we will use this as our cities_to_add above
    distance_matrix = getDistanceMatrix(cities) #returns a matrix of city distances

    #Retreive the total distance travelled and the path
    totalDistance, thePath = findBestPath(distance_matrix, cities_copy)

    #Get distance for drive home from the last city to starting city.
    totalDistance += getDistanceForTripHome(thePath, cities)

    #Write to output file
    outFile = open(inputFile + ".tour", 'w')
    print>>outFile, totalDistance
    for node in thePath:
        print>>outFile, node
