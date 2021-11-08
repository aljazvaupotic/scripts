## Kalkulator tort za Uršiko
import math
import json
## Volume
def area (diameter):
    return math.pi* ((diameter/2)**2)

def dif(theirVol, myVol):
    return myVol/theirVol
n = int (input("Njihov pekač: "))
m = int (input("Tvoj pekač: "))
d = (dif(area(n),area(m)))
print(d)
ing = {}
s = ""
print("Vnesi recept ločen z : ")
while(True) :
    s = input("") 
    if(s == "x"):
        break
    x = s.split(":")
    ing[x[0]] = int(x[1])

mying = ing.copy()
for k in mying:
    mying[k] = mying.get(k) * d
#print(ing)
#print()
k = input("Ime recepta")
f = open(k+".txt", "a")
f.write("Potrebne količine za moj pekač\n\n")
#y = json.dumps(mying)
#f.write(y)
for x, y in mying.items():
    s = str(x) + " : " + str(round(y,2));
    f.write(s + "\n")
    #print(x, round(y,2))
f.close()