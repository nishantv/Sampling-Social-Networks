"""
runSim.py
runs Simulator.py with necessary arguments and saves output
"""

import os
import datetime

def main():
  NUMTRIES = 5 #number of times to run Simulator.py
  INPUT = "Email-Enron.txt"
  NUMHOPS = 20
  OUTPUTFILE = "output.txt"
  os.system("date")
  print("Number of trials: %s  Dataset: %s Number of hops: %s")%(NUMTRIES, INPUT, NUMHOPS)
  for i in range(NUMTRIES):
    print ("\nTrial: %s\n"%(i+1))
    os.system("python Simulator.py %s %s"%(INPUT, NUMHOPS))
    print("__________________________\n\n")

if __name__ == "__main__":
  main()
