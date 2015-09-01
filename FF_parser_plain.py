# This software is in the public domain because it contains materials that
# originally came from the U.S. Geological Survey, an agency of the United
# States Department of Interior.
# For more information, see the official USGS copyright policy at
# http://www.usgs.gov/visual-id/credit_usgs.html#copyright

# Although this software program has been used by the U.S. Geological Survey
# (USGS), no warranty, expressed or implied, is made by the USGS or the U.S.
# Government as to the accuracy and functioning of the program and related
# program material nor shall the fact of distribution constitute any such
# warranty, and no responsibility is assumed by the USGS in connection therewith.

# This software is provided "AS IS."
#*******************************************************************************
# author - Andrew Bock, Colorado Water Science Center, Denver Federal Center,
#          PO Box 25046, MS 415, Denver, CO, 80225
# email: abock@usgs.gov
# phone: (815)236-3039
#*******************************************************************************

# reads line in the file
def readLine(linenum,infile):
    rfile = open(infile,"r")
    rlines = rfile.readlines()[linenum]
    items = rlines.split()
    return items[1:]

# reads multiple lines in file
def readMultLines(linenum,infile):
    retList=[]
    for num in linenum:
        rfile = open(infile,"r")
        rlines = rfile.readlines()[num]
        items = rlines.split()
        retList.append(items[1])
        rfile.close()
    return retList

# read in necessary modules
import os, numpy,glob, ctypes

# set the working directory to the location of the script
thisdir = os.getcwd()
#dirsfiles = os.listdir(thisdir)
# find flood frequency files and put them into a list
FF_files=glob.glob("*.EXP")

# message box for errors (if no .EXP files in folder location)
if len(FF_files)==0:
    msg=ctypes.windll.user32.MessageBoxA(None,"Please put program in the proper folder location with the .EXP"," ",0,uType="MB_SETFOREGROUND | MB_ICONINFORMATION | MB_OK")
    sys.exit("Please put program in the proper folder location with the Flood Frequency Files")
else:
    msg=ctypes.windll.user32.MessageBoxA(None,str(len(FF_files))+" sites to be processed?","WARNING",4,uType="MB_SETFOREGROUND")
	# line number which hold the statistics
    Stats=[7,9,14,16]
    ExcProb=21
    Estimates=22
    Kval=26

	# create empty lists and matrices to hold data
    Gages=[]
    Sdf=numpy.zeros(shape = (len(FF_files),4))
    EPdf=numpy.zeros(shape = (len(FF_files),25))
    Estdf=numpy.zeros(shape = (len(FF_files),25))
    Kdf=numpy.zeros(shape = (len(FF_files),25))

	# loop through files and retrieve data
    # put data into lists and matrices
    count = 0
    for gfile in FF_files:
        Gages.append(gfile.split(".")[0])
        print gfile
        EP=readLine(ExcProb,gfile)
        EPdf[count,]=EP
        Est=readLine(Estimates,gfile)
        Estdf[count,]=Est
        K=readLine(Kval,gfile)
        Kdf[count,]=K
        S = readMultLines(Stats,gfile)
        Sdf[count,]=S
        count = count+1

    # write output files
    out_Sdf = open("Stats.txt","w")
    out_Edf = open("ExProb.txt","w")
    out_Estdf = open("Est.txt","w")
    out_Kdf = open("KValue.txt","w")
    Sheader = "gage Skew StandDev RegSkew SysPeaks\n"
    out_Sdf.writelines(Sheader)
    for i in range(0,len(Gages)):
        Sline = Sdf
        #current_var_float=[float(x) for x in current_var_str]
        line1 = Gages[i]+' '+' '.join(str(x) for x in Sdf[i,])+'\n'
        out_Sdf.writelines(line1)
        line2 = Gages[i]+' '+' '.join(str(x) for x in EPdf[i,])+'\n'
        out_Edf.writelines(line2)
        line3 = Gages[i]+' '+' '.join(str(x) for x in Estdf[i,])+'\n'
        out_Estdf.writelines(line3)
        line4 = Gages[i]+' '+' '.join(str(x) for x in Kdf[i,])+'\n'
        out_Kdf.writelines(line4)
    out_Sdf.close()
    out_Edf.close()
    out_Estdf.close()
    out_Kdf.close()
