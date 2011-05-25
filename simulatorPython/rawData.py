"""
Code to pull out raw data from datasets
Current measures: degree distribution
"""
from __future__ import division
import sys
import os
import utilities

def getRawData(fileName):
  opfile = "rawData/rawDataDegree_%s"%fileName
  degDistFile = "rawData/rawDataDistribution_%s"%fileName
  distDict = {}   #distribution count
  Graph = utilities.getGraph(fileName)
  graphNodes = Graph.keys()
  for neighborList in Graph.values():
    degree = len(neighborList)
    if distDict.has_key(degree):
      distDict[degree] += 1
    else:
      distDict[degree] = 1
  fp = open(opfile, "w")
  fp2 = open(degDistFile, "w")
  for node in graphNodes:
    fp.write("%s\t%s\n"%(node, len(Graph[node])))
    fp2.write("%s\t%s\t%s\n"%(len(Graph[node]), \
    distDict[len(Graph[node])], distDict[len(Graph[node])] / len(Graph))) 
  """
  """
  fp.close()
  fp2.close()
  print ("Files saved: %s, %s"%(opfile, degDistFile))

def main():
  try:
    fileName = sys.argv[1]
  except:
    printError()
  if os.path.exists(fileName):
    if not os.path.exists('rawData'): os.mkdir('rawData')
    getRawData(fileName)
  else: 
    printError()

def printError():
  print "usage: python Simulator.py <input filename>\
        \n\tTry again..."
  sys.exit(1)

if __name__ == "__main__":
  main()
