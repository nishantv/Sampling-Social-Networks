import sys
import random
import os
import utilities
import cProfile 
from collections import deque
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

NUMITERATIONS = 28

def analyzeGraph(fileName, numHops):
  os.system("clear")
  print outputDir
  Graph = utilities.getGraph(fileName)
  #Graph = loadGraph()
  graphNodes = Graph.keys()
  visitedNodes = set()
  currIndex = 1
  while currIndex <= NUMITERATIONS:
    startIdx = random.randint(0, len(graphNodes))
    startNode = graphNodes[startIdx]
    if startNode not in visitedNodes:
      print "Random Walk"
      runRW(startNode, numHops, Graph, currIndex)
      print "Uniform sample"
      getUniformSample(numHops, Graph, currIndex)
      print "BFS"
      #runBFS(startNode, numHops, Graph, currIndex)
      bfs(startNode, numHops, Graph, currIndex)
      print "RDS"
      try:
        runRDS(startNode, numHops, Graph, currIndex)
      except:
        print "RDS: StartNode %s Run %s bombed......................."%(startNode, currIndex)
      currIndex += 1
  """
  startIdx = random.randint(0, len(graphNodes))   #FIXME start node should be explicit 
  startNode = graphNodes[startIdx]
  print "startIdx = %s, startNode = %s"%(startIdx, startNode)
  print "Random Walk"
  ##RWalkDict, RWalkList = runRW(startNode, numHops, Graph, ITERNUM)
  ##print RWalkDict
  ##zEst = utilities.getZEstimate(RWalkList, Graph)
  ##print "Z-estimate = %s"%zEst
  runRW(startNode, numHops, Graph, ITERNUM)
  print "Uniform sample:"
  ##UNI = getUniformSample(numHops, Graph, ITERNUM)
  ##print UNI
  getUniformSample(numHops, Graph, ITERNUM)
  print "BFS"
  ##BFSWalk = runBFS(startNode, numHops, Graph, ITERNUM)
  ##print BFSWalk
  runBFS(startNode, numHops, Graph, ITERNUM)
  """
def runRW(startNode, numHops, Graph, ITERNUM):
  runType = "RandomWalk"
  fileName = "%s/%s_%s_%s.txt"%(outputDir, runType, numHops, ITERNUM)
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
  ##print "Random Walk done."## Walked nodes: %s"%walkedNodes
  ##print "Number of nodes walked: %s Number of unique nodes: %s"\
  ##%(len(walkedNodes), len(set(walkedNodes)))
  ##for node in set(walkedNodes): 
    ##distDict[node] = len(Graph[node])   
    #print node, len(Graph[node])
  print "%s saved... "%fileName
  fp.close()
  ##return distDict, utilities.getSet(walkedNodes)

def runBFS(startNode, numHops, Graph, ITERNUM, path=[]):
  runType = "BFS"
  pathDict = {}
  fileName = "%s/%s_%s_%s.txt"%(outputDir, runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  q=[startNode]
  while q:
    v=q.pop(0)
    #if not v in path:
    if not pathDict.has_key(v):
      pathDict[v] = 1
      path=path+[v]
      q=q+Graph[v]
    if len(path) > numHops:
      ##distDict = {}
      for node in path: 
        ##distDict[node] = len(Graph[node])
        fp.write("%s\t%s\n"%(node, len(Graph[node]) ) )
      print "%s saved... "%fileName
      fp.close()
      return True
      ##return distDict

def bfs(startNode, numHops, Graph, ITERNUM):
  """
  Implementation of BFS using collections
  """
  runType = "BFS"
  fileName = "%s/%s_%s_%s.txt"%(outputDir, runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  queue, enqueued = deque([(None, startNode)]), set([startNode])
  while queue:
    if len(enqueued) > numHops:
      #print type(enqueued), len(enqueued)
      for node in enqueued:
        fp.write("%s\t%s\n"%(node, len(Graph[node]) ) )
      print "%s saved... "%fileName
      fp.close()
      return 
    parent, n = queue.popleft()
    #yield parent, n 
    new = set(Graph[n]) - enqueued
    enqueued |= new
    queue.extend([(n, child) for child in new])


def getUniformSample(numHops, Graph, ITERNUM):
  runType = "UNI"
  fileName = "%s/%s_%s_%s.txt"%(outputDir, runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  uniformSample = []
  UNIDict = {}
  nodes = Graph.keys()
  for i in range(numHops):
    uniformSample.append(random.choice(nodes))
  ##print "%s samples, %s unique samples"%(len(uniformSample), \
  ##len(set(uniformSample)))
  for node in uniformSample: 
    ##UNIDict[node] = len(Graph[node])
    fp.write("%s\t%s\n"%(node, len(Graph[node]) ) )
  print "%s saved... "%fileName
  fp.close()
  ##return UNIDict

def runRDS(startNode, numHops, Graph, ITERNUM):
  runType = "RDS"
  fileName = "%s/%s_%s_%s.txt"%(outputDir, runType, numHops, ITERNUM)
  fp = open(fileName, "w")
  walkedNodes = []
  nodeQ = []
  triedNodes = set()
  currNode = startNode
  walkedNodes.append(currNode)
  nodeQ += [currNode]
  currNeighbors = Graph[currNode]
  while (len(walkedNodes) < numHops):
    #currNeighbors = Graph[currNode]
    if len(currNeighbors) < 4:
      for node in currNeighbors:
        if node not in triedNodes:
          nodeQ += [node]
          triedNodes.add(node)
    else: #pasting Harish's code
      for j in range (1, 4):
        i = random.randint(0, (len(currNeighbors) - j) )
        if (currNeighbors[i] not in triedNodes):
          triedNodes.add(currNeighbors[i])
          nodeQ += [currNeighbors[i]]
          currNeighbors.append ( currNeighbors.pop(i) )
    #print "Qlen = %s"%len(nodeQ)
    currNode = nodeQ.pop(0)
    p = random.random()
    if (p > 0.33) and currNode not in walkedNodes:
      walkedNodes.append(currNode)
      fp.write("%s\t%s\n"%(currNode, len(Graph[currNode])))
    currNeighbors = Graph[currNode]
  print "%s saved... "%fileName
  fp.close()

def main():
  try:
    fileName, numHops = sys.argv[1], sys.argv[2]
  except:
    printError()
  if os.path.exists(fileName):
    global outputDir
    outputDir = "%s/outputs"%(fileName.split(".")[0]) 
    if not os.path.exists(outputDir): os.makedirs(outputDir)
    analyzeGraph(fileName, int(numHops))
  else: 
    printError()

def printError():
  print "usage: python Simulator.py <input filename> <number of hops>\
        \n\tTry again..."
  sys.exit(1)
   
if __name__ == "__main__":
  main()

