import sys

print ("Inside python")
Emaxs = []
for k in range(len(sys.argv)):
    if (len(sys.argv) - k) == 1:
        break
    Emaxs.append(float(sys.argv[k+1]))

print (Emaxs)
