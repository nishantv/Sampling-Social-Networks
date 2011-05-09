import sys
import cPickle
import random

"""
Loads a graph from file, pickles it and returns the 
graph as an adjacency list
"""
def populateGraph(fp):
  Graph = {}
  for line in fp:
    first, second = line.split("\t")
    Graph.setdefault(int(first), []).append(int(second))
  cPickle.dump(Graph, open("graph.pkl","w"))
  print "ok"
  return Graph

"""
Loads a graph from file; adjacency list
"""
def getGraph(fp):
  print "Loading graph... "
  Graph = {}
  for line in fp:
    try:
      first, second = line.rstrip("\n").split("\t")
      Graph.setdefault(int(first), []).append(int(second))
    except: print line #pass
  print "Graph loaded!"
  return Graph  

"""
Loads and returns a pickled graph object
"""
def loadGraph():
  print "Loading pickled graph..."
  Graph = cPickle.load(open("graph.pkl"))
  print "Graph loaded..."  
  return Graph

"""
'Heart' of the code
Performs a naive random walk from a random seed node
"""
def analyzeGraph(fp, numHops):
  Graph = getGraph(fp)
  #Graph = loadGraph()
  graphNodes = Graph.keys()
  startIdx = random.randint(0, len(graphNodes))   #FIXME start node should be explicit 
  startNode = graphNodes[startIdx]
  print "startIdx = %s, startNode = %s"%(startIdx, startNode)
  #runBFS(Graph, startNode)
  print "Random Walk"
  RWalk = runRW(startNode, numHops, Graph)
  print RWalk
  print "Uniform sample:"
  UNI = getUniformSample(numHops, Graph)
  print UNI
  print "BFS"
  BFSWalk = runBFS(startNode, numHops, Graph)
  print BFSWalk

def runRW(startNode, numHops, Graph):
  walkedNodes = []
  distDict = {} #creating the distribution dictionary for plotting(RW)
  currNode = startNode
  #print "Starting walk..."
  while (len(walkedNodes) < numHops + 1):
    walkedNodes.append(currNode)
    currNeighbors = Graph[currNode]
    currNode = currNeighbors[random.randint(0, len(currNeighbors)) - 1]
  print "Random Walk done. Walked nodes: %s"%walkedNodes
  print "Number of nodes walked: %s Number of unique nodes: %s"\
  %(len(walkedNodes), len(set(walkedNodes)))
  for node in set(walkedNodes): 
    distDict[node] = len(Graph[node])   
    #print node, len(Graph[node])
  plotGraph(distDict, "RandomWalk")
  return distDict

"""
def runBFS(Graph, startNode, numHops):
  walkedNodes = []
  currNode = startNode
  while len(walkedNodes < numHops):
    walkedNodes.append(currNode)
    currNeighbors = Graph[currNode]
    for node in currNeighbors: walkedNodes.append(node)
  pass
"""

def runBFS(startNode, numHops, Graph, path=[]):
  q=[startNode]
  while q:
    v=q.pop(0)
    if not v in path:
      path=path+[v]
      q=q+Graph[v]
    if len(path) > numHops:
      distDict = {}
      for node in path: 
        distDict[node] = len(Graph[node])
      plotGraph(distDict, "BFS") 
      return distDict

def getUniformSample(numHops, Graph):
  uniformSample = []
  UNIDict = {}
  nodes = Graph.keys()
  for i in range(numHops):
    uniformSample.append(random.choice(nodes))
  print "%s samples, %s unique samples"%(len(uniformSample), \
  len(set(uniformSample)))
  for node in uniformSample: UNIDict[node] = len(Graph[node])
  #print UNIDict
  plotGraph(UNIDict, "UniformSample")
  return UNIDict

def plotGraph(distDict, walkType):
  import matplotlib
  import numpy as np
  import matplotlib.pyplot as plt
  fileName = "walk_%s.png"%(walkType)
  fig = plt.figure()
  #N=200
  print "Plotting %s distribution..."%walkType
  #nodes = distDict.keys()
  neighbors = distDict.values()
  N = max(neighbors)
  #creating values for frequency plot
  samples = np.array(neighbors)
  n, bins, patches  = plt.hist( samples, N, facecolor="magenta",\
                                  range=[1,N], normed=True )
  plt.xlabel('Degree')
  plt.ylabel('Probability')  
  fig.savefig(fileName)
  print "plot saved at %s"%fileName

def main():
  try:
    fileName, numHops = sys.argv[1], sys.argv[2]
    fp = open(fileName)
  except:
    print "usage: python Simulator.py <input filename> <number of hops>\
          \n\tTry again..."
    sys.exit(1)
#  populateGraph(fp)
  analyzeGraph(fp, int(numHops))
   
if __name__ == "__main__":
  main()

