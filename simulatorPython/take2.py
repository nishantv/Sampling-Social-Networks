import sys

def analyzeGraph(fp):
#  while (fp.readline()):
#    line = fp.readline()
#    first, second = line.split('\t')
#    print first, second
  lines = (fp.read()).split("\n")
  for line in lines: 
    try:
        

def main():
  try:
    fileName = sys.argv[1]
    fp = open(fileName)
  except:
    print "usage: python take2.py <input filename>\n\tTry again..."
    sys.exit(1)
  analyzeGraph(fp)
   
if __name__ == "__main__":
  main()
