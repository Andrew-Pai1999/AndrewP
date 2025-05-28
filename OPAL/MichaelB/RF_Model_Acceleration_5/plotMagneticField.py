import matplotlib.pyplot as plt
import numpy as np 
import math
import itertools

print("Hello Cruel World")

f=open("85percentField.dat")
lines=f.readlines()[0:6]
#lines2=f.readlines()[7:9]
f.close()
#this seems redundant but it did not seem to work when I did 2 readlines for 1 file open...
f=open("85percentField.dat")
#lines=f.readlines()[0:6]
lines2=f.readlines()[6:]
f.close()


#print(lines)
Rmin=int(lines[0]) #set to 0
deltaR=float(lines[1]) #  set to 24.13
thetaMin=float(lines[2])  #set to 0
deltaTheta=int(lines[3])  # set to 2
Ntheta=int(lines[4]) # total data number in each arc path of azimuthal direction  2*180=360
Nr=int(lines[5]) #total path number along radial direction  set to 40*24.13=965.2

print(Rmin)

#So if I want to read Radius 1 I need to read the first 180 or Ntheta numbers after line 6 including line 1 as line 0

this=[]
this1=[]

#lines2.rstrip()

#print("lines2 is ", lines2)
for line in lines2:
   this.append(line.split())
   #this1.append(float(line.rstrip()))
   
print("Length of this[0] is ")
lineLength=len(this[0])
print(lineLength)
numberOfLines=int(Ntheta*Nr/lineLength)
print("number of lines is ", numberOfLines)


for j in range(0,numberOfLines):
    for i in range(0,len(this[0])):
        this1.append(this[j][i])

#There are 40 different Radii based on parameter Nr so if I divide that into 10 equal radii then it is 40/10 or 4
tcRange=Nr/10


#Lets split it up into 10 orbit ranges
#tc1=this1[0:int(5.0)]  #for Trim Coil #1
tc1=this1[0:int(1*(Nr/10)*Ntheta)]  #for Trim Coil #1
tc2=this1[int(1*(Nr/10)*Ntheta):int(2*(Nr/10)*Ntheta)]  #for Trim Coil #2
tc3=this1[int(2*(Nr/10)*Ntheta):int(3*(Nr/10)*Ntheta)]  #for Trim Coil #3
tc4=this1[int(3*(Nr/10)*Ntheta):int(4*(Nr/10)*Ntheta)]  #for Trim Coil #4
tc5=this1[int(4*(Nr/10)*Ntheta):int(5*(Nr/10)*Ntheta)]  #for Trim Coil #5
tc6=this1[int(5*(Nr/10)*Ntheta):int(6*(Nr/10)*Ntheta)]  #for Trim Coil #6
tc7=this1[int(6*(Nr/10)*Ntheta):int(7*(Nr/10)*Ntheta)]  #for Trim Coil #7
tc8=this1[int(7*(Nr/10)*Ntheta):int(8*(Nr/10)*Ntheta)]  #for Trim Coil #8
tc9=this1[int(8*(Nr/10)*Ntheta):int(9*(Nr/10)*Ntheta)]  #for Trim Coil #9
tc10=this1[int(9*(Nr/10)*Ntheta):int(10*(Nr/10)*Ntheta)]  #for Trim Coil #10
print("tc1 is ")
print(len(tc2))

##############################################################################################
##########   Now we print a new scaled field map     #########################################
##############################################################################################

f=open('newfield.dat', 'w')
#f.write("hey Dude")
f.write(str(Rmin)+"\n")
f.write(str(deltaR)+"\n")
f.write(str(thetaMin)+"\n")
f.write(str(deltaTheta)+"\n")
f.write(str(Ntheta)+"\n")
f.write(str(Nr)+"\n")

#TC1scale=1.0
#TC2scale=1.0
#TC3scale=.990
#TC4scale=.985
#TC5scale=.980
#TC6scale=.975
#TC7scale=.970
#TC8scale=.965
#TC9scale=.960
#TC10scale=.955

#y=mx+b


TC1scale=1.002
TC2scale=1.003
TC3scale=1.002
TC4scale=1.002
TC5scale=1.004                     #       1.000000001
TC6scale=1.003
TC7scale=1.003
TC8scale=1.001
TC9scale=1.000
TC10scale=1.000
newField1=[]
j=0
z=0
for i in range(0,len(tc1)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0 
        z=2    #this was just to get rid of a space at the first line         
    #print(tc1[i])
    #print(str(TC1scale*float(tc1[i])))
    f.write(str(round(TC1scale*float(tc1[i]),5)))
    #f.write(" ")
    j=j+1

for i in range(0,len(tc2)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc2[i])
    #print(str(TC2scale*float(tc2[i])))
    f.write(str(round(TC2scale*float(tc2[i]),5)))
    #f.write(" ")
    j=j+1

for i in range(0,len(tc3)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc3[i])
    #print(str(TC3scale*float(tc3[i])))
    f.write(str(round(TC3scale*float(tc3[i]),5)))
    #f.write(" ")
    j=j+1    

for i in range(0,len(tc4)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc4[i])
    #print(str(TC4scale*float(tc4[i])))
    f.write(str(round(TC4scale*float(tc4[i]),5)))
    #f.write(" ")
    j=j+1    
    

for i in range(0,len(tc5)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc5[i])
    #print(str(TC5scale*float(tc5[i])))
    f.write(str(round(TC5scale*float(tc5[i]),5)))
    #f.write(" ")
    j=j+1  

for i in range(0,len(tc6)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc6[i])
    #print(str(TC6scale*float(tc6[i])))
    f.write(str(round(TC6scale*float(tc6[i]),5)))
    #f.write(" ")
    j=j+1      

for i in range(0,len(tc7)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc7[i])
    #print(str(TC7scale*float(tc7[i])))
    f.write(str(round(TC7scale*float(tc7[i]),5)))
    #f.write(" ")
    j=j+1      

for i in range(0,len(tc8)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc8[i])
    #print(str(TC8scale*float(tc8[i])))
    f.write(str(round(TC8scale*float(tc8[i]),5)))
    #f.write(" ")
    j=j+1      

for i in range(0,len(tc9)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc9[i])
    #print(str(TC9scale*float(tc9[i])))
    f.write(str(round(TC9scale*float(tc9[i]),5)))
    #f.write(" ")
    j=j+1      

for i in range(0,len(tc10)):
    if j!=5:
         f.write(" ")
    if j==5:
        f.write("\n")
        j=0             
    #print(tc10[i])
    #print(str(TC10scale*float(tc10[i])))
    f.write(str(round(TC10scale*float(tc10[i]),5)))
    #f.write(" ")
    j=j+1      
   
#f.write(newField1)

f.close()