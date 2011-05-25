import os

#outpath = "Email-Enron/frequencies"
outpath = "soc-Epinions1/outputs"

def getDistributions():
  #inpath = "Email-Enron/outputs"
  inpath = "soc-Epinions1/outputs"
  if not os.path.exists(outpath): os.mkdir(outpath)
  for (_, _, files) in os.walk(inpath):
    for fileName in files: 
      getFrequencies("%s/%s"%(inpath,fileName))

def getFrequencies(fileName):
  print fileName
  freqDict = {}
  fp = open(fileName)
  frequencyFile = fileName.split("/")[2].replace(".txt","_Distribution.txt")
  freqFP = open("%s/%s"%(outpath, frequencyFile), "w")
  print "%s/%s"%(outpath, frequencyFile)
  for line in fp:
    _, degree = line.split("\t")
    if freqDict.has_key(degree):
      freqDict[degree] += 1
    else:
      freqDict[degree] = 1
  for k,v in freqDict.items():
    freqFP.write("%s\t%s\n"%(int(k),v))
  freqFP.close()
  fp.close()

def main():
  getDistributions()

if __name__ == "__main__":
  main()
