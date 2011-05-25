"""
Contains utilities for running Simulator.py
"""
from __future__ import division
import cPickle
import os
import math

def getSet(someList):
  """
  The set() operation ruins the order of the walks, so reimplementing
  """
  newList = []
  for item in someList: 
    if (not item in newList): newList.append(item)
  return newList

def getGraph(fileName):
  pickleFileName = fileName.replace("txt","pkl")
  if os.path.exists(pickleFileName): return getPickledGraph(pickleFileName)
  else:   #load graph and pickle it
    print "Loading graph... "
    Graph = {}
    fp = open(fileName)
    for line in fp:
      if "#" in line: pass
      else:
        try:
          first, second = (line.rstrip("\n").split("\t"))[:2]
          Graph.setdefault(int(first), []).append(int(second))
          #uncomment the line below if the graph is undirected #FIXME
          #FIXME: add command line check for directed graphs
          Graph.setdefault(int(second), []).append(int(first))
        except: print line #pass
    cPickle.dump(Graph, open(pickleFileName,"w"))
    print "Graph loaded! Graph size: %s"%(len(Graph))
    return Graph 

"""
Loads and returns a pickled graph object
"""
def getPickledGraph(pickleFileName):
  print "Loading pickled graph..."
  Graph = cPickle.load(open(pickleFileName))
  return Graph

def getZEstimate(walkedList, Graph):
  #walkedList = walkedPath.keys()
  print "Z-estimates:"
  print len(walkedList)//10
  print len(walkedList)//2
  Xa = walkedList[:(len(walkedList)//10)]
  Xb = walkedList[(len(walkedList)//2):]
#  print "Xa:%s\nXb:%s"%(Xa, Xb)
  zEstimate = getExpectation(Xa, Graph) - getExpectation(Xa, Graph)/ \
              math.sqrt( getVariance(Xa, Graph) + getVariance(Xb, Graph) )
  return zEstimate

def getExpectation(someList, Graph):
  #degreeList = [len(Graph[node]) for node in someList]
  #return sum(degreeList) / len(someList)
  vals = 0
  for node in someList:
    vals += len(Graph[node])
  return vals / len(someList)


def getVariance(someList, Graph):
  vals, varianceVals = 0, 0
#  degreeList = [len(Graph[node]) for node in someList]
#  mean = sum(degreeList) / len(someList)
#  varList = [(degree - mean) ** 2 for degree in degreeList]
#  return sum(varList) / len(someList)
  vals = 0
  for node in someList:
    vals += len(Graph[node])
  mean = vals / len(someList)
  for node in someList:
    varianceVals += ( (len(Graph[node]) - mean) **2 )
  return varianceVals / len(someList)

