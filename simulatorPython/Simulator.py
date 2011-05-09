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
  UNIDict = {} #creating the distribution dictionary for plotting(UNI)
  graphNodes = Graph.keys()
  startIdx = random.randint(0, len(graphNodes))   #FIXME start node should be explicit 
  startNode = graphNodes[startIdx]
  print "startIdx = %s, startNode = %s"%(startIdx, startNode)
  #runBFS(Graph, startNode)
  RWDistribution = runRW(startNode, numHops, Graph)
  print "Random Walk"
  print RWDistribution
  UNI = getUniformSample(numHops, Graph)
  print "Uniform sample:"
  print "%s samples, %s unique samples"%(len(UNI), len(set(UNI)))
  for node in UNI: UNIDict[node] = len(Graph[node])
  print UNIDict

def runRW(startNode, numHops, Graph):
  walkedNodes = []
  distDict = {} #creating the distribution dictionary for plotting(RW)
  currNode = startNode
  print "Starting walk..."
  while (len(walkedNodes) < numHops + 1):
    walkedNodes.append(currNode)
    currNeighbors = Graph[currNode]
    currNode = currNeighbors[random.randint(0, len(currNeighbors)) - 1]
  print "Walk done. Walked nodes: %s"%walkedNodes
  print "Number of nodes walked: %s Number of unique nodes: %s"\
  %(len(walkedNodes), len(set(walkedNodes)))
  for node in set(walkedNodes):
    distDict[node] = len(Graph[node])   
    #print node, len(Graph[node])
  return distDict
  #plotGraph(distDict)

def runBFS(Graph, startNode):
  pass

def getUniformSample(numHops, Graph):
  uniformSample = []
  nodes = Graph.keys()
  for i in range(numHops):
    uniformSample.append(random.choice(nodes))
  return uniformSample

def plotGraph(distDict):
  import matplotlib
  import numpy as np
  import matplotlib.pyplot as plt
  fig = plt.figure()
  N=20
  #nodes = distDict.keys()
  neighbors = distDict.values()
  #creating values for frequency plot
  samples = np.array(neighbors)
  n, bins, patches  = plt.hist( samples, N, facecolor="magenta",\
                                  range=[1,N], normed=True )
  plt.xlabel( 'bins' )
  plt.ylabel( 'Probability' )  
  fig.savefig('test.png')
  print "saved"

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

