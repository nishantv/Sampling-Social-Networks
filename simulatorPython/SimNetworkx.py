import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

def analyzeGraph(fp, numHops):
  print "Loading graph"
  G = nx.Graph()
  nodeSet = set()
  try:
    for line in fp:
      first, second = line.split("\t")
      if not (first in nodeSet): 
        nodeSet.add(first)
        G.add_node(first)  
      if not (second in nodeSet): 
        nodeSet.add(second)  
        G.add_node(second)
      G.add_edge(first, second)
  except: print line  
  print "Graph loaded"
  print "Number of nodes: %s, Number of edges: %s"% \
  (G.number_of_nodes(), G.number_of_edges())
  plotGraph(G)

def plotGraph(G):
  print "Plotting..."
  #plt.figure(1,figsize=(8,8))
  pos=nx.graphviz_layout(G,prog="neato")
  nx.draw(G, pos)
  plt.savefig("enron.png",dpi=75)

def main():
  try:
    fileName, numHops = sys.argv[1], sys.argv[2]
    fp = open(fileName)
  except:
    print "usage: python Simulator.py <input filename> <number of hops>\n\tTry again..."
    sys.exit(1)
#  populateGraph(fp)
  analyzeGraph(fp, int(numHops))
   
if __name__ == "__main__":
  main()

