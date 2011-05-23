import sys
import random
import os
import utilities
import cProfile 
#import matplotlib
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import pylab 

"""
'Heart' of the code
Performs:
1) Naive random walk from a random seed node
2) Generates a uniform sample (rejection based)
3) BFS
"""

ITERNUM = 1 #currently hardcoding. 
"""
Ideally, the driver module should pass ITERNUM to the crawl modules
"""



def analyzeGraph(fileName, numHops):
  os.system("clear")
  Graph = utilities.getGraph(fileName)
  #Graph = loadGraph()
  graphNodes = Graph.keys()
  startIdx = random.randint(0, len(graphNodes))   #FIXME start node should be explicit 
  startNode = graphNodes[startIdx]
  print "startIdx = %s, startNode = %s"%(startIdx, startNode)

  print "Random Walk"
  RWalkDict, RWalkList = runRW(startNode, numHops, Graph, ITERNUM)
  print RWalkDict
  zEst = utilities.getZEstimate(RWalkList, Graph)
  print "Z-estimate = %s"%zEst

  print "Uniform sample:"
  UNI = getUniformSample(numHops, Graph, ITERNUM)
  print UNI

  print "BFS"
  BFSWalk = runBFS(startNode, numHops, Graph, ITERNUM)
  print BFSWalk
  
def runRW(startNode, numHops, Graph, ITERNUM):
  runType = "RandomWalk"
  fileName = "outputs/%s_%s_%s.txt"%(runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  walkedNodes = []
  distDict = {} #creating the distribution dictionary for plotting(RW)
  currNode = startNode
  #print "Starting walk..."
  while (len(walkedNodes) < numHops + 1):
    walkedNodes.append(currNode)
    fp.write("%s\t%s\n"%(currNode, len(Graph[currNode]) ) )
    currNeighbors = Graph[currNode]
    currNode = currNeighbors[random.randint(0, len(currNeighbors)) - 1]
  print "Random Walk done. Walked nodes: %s"%walkedNodes
  print "Number of nodes walked: %s Number of unique nodes: %s"\
  %(len(walkedNodes), len(set(walkedNodes)))
  for node in set(walkedNodes): 
    distDict[node] = len(Graph[node])   
    #print node, len(Graph[node])
  fp.close()
  return distDict, utilities.getSet(walkedNodes)

def runBFS(startNode, numHops, Graph, ITERNUM, path=[]):
  runType = "BFS_"
  fileName = "outputs/%s_%s_%s.txt"%(runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  q=[startNode]
  while q:
    v=q.pop(0)
    if not v in path:
      path=path+[v]
      q=q+Graph[v]
      #print v,
    if len(path) > numHops:
      distDict = {}
      for node in path: 
        distDict[node] = len(Graph[node])
        fp.write("%s\t%s\n"%(node, len(Graph[node]) ) )
      fp.close()
      return distDict

def getUniformSample(numHops, Graph, ITERNUM):
  runType = "UNI_"
  fileName = "outputs/%s_%s_%s.txt"%(runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  uniformSample = []
  UNIDict = {}
  nodes = Graph.keys()
  for i in range(numHops):
    uniformSample.append(random.choice(nodes))
  print "%s samples, %s unique samples"%(len(uniformSample), \
  len(set(uniformSample)))
  for node in uniformSample: 
    UNIDict[node] = len(Graph[node])
    fp.write("%s\t%s\n"%(node, len(Graph[node]) ) )
  fp.close()
  return UNIDict

def main():
  try:
    fileName, numHops = sys.argv[1], sys.argv[2]
  except:
    printError()
  if os.path.exists(fileName):
    if not os.path.exists('outputs'): os.mkdir('outputs')
    analyzeGraph(fileName, int(numHops))
  else: 
    printError()

def printError():
  print "usage: python Simulator.py <input filename> <number of hops>\
        \n\tTry again..."
  sys.exit(1)
   
if __name__ == "__main__":
  main()

