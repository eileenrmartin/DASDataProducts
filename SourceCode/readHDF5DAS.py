# Author: Eileen R. Martin, eileenrmartin@vt.edu
# Last Modified: July 10, 2019

# read an hdf5 file 
# example: hdf5data/Test001/20m_S2019-06-04T20_12_18_512sw256ssSeg16/20m_S2019-06-04T20_12_18_TimeResponse.h5
# Run as:
# python readHDF5DAS.py filenameWithPath

import sys
import numpy as np
import h5py 
import matplotlib.pyplot as plt
plt.switch_backend('agg')

inputFile = sys.argv[1]

#parsedFilePath = inputFile.split('/')
#exampleName = parsedFilePath[1]
exampleName = 'ExampleData'
print("============================================")
print("Starting plots related to "+inputFile)
hf = h5py.File(inputFile, 'r')
dataList = list(hf.keys()) # should contain 'data' and 'timing(s)' and 'locations(m)'

timingH5 = hf.get('timing(s)')
timing = np.array(timingH5)
print('timing array shape (nWindows, nTimesPerWindow): '+str(timing.shape))
nWindows = timing.shape[0]
nTimesPerWindow = timing.shape[1]

print('timing'+str(timing))


locationH5 = hf.get('locations(m)')
location = np.array(locationH5)
print('location array shape (nChannels,): '+str(location.shape))

dataH5 = hf.get('data')
data = np.array(dataH5)
print('data array shape (nWindows, nTimesPerWindow, nChannels): '+str(data.shape))
nChannels = data.shape[2]

print("------Attributes of the data------")
attrList = list(dataH5.attrs)
for attr in attrList:
	print(attr+'\t \t'+str(dataH5.attrs[attr]))

hf.close()

# plot a few windows of data
sliceID = 20
dataOfInterest = data[sliceID,:,:]
clip = np.percentile(np.absolute(dataOfInterest),95)
plt.imshow(dataOfInterest,aspect='auto',interpolation='nearest',vmin=-clip,vmax=clip,cmap=plt.get_cmap('seismic'))
plt.colorbar()
plt.xlabel('channel index')
plt.ylabel('time sample')
plt.title('time window number '+str(sliceID))
plt.savefig('fig/firstTest' + exampleName)
plt.clf()

channelID = 100
dataOfInterest = data[:,:,channelID]
clip = np.percentile(np.absolute(dataOfInterest),97)
plt.imshow(dataOfInterest,aspect='auto',interpolation='nearest',vmin=-clip,vmax=clip,cmap=plt.get_cmap('seismic'))
plt.colorbar()
plt.ylabel('window number')
plt.xlabel('time sample in window')
plt.title('channel '+str(channelID))
plt.savefig('fig/secondTest' + exampleName)
plt.clf()

# stack a few windows of data
startSlice = 5
endSlice = 25
#timeBetweenWindows = timing[startSlice+1,0]-timing[startSlice,-1]
#timeBetweenSamples = timing[startSlice,1]-timing[startSlice,0]
#gapTimeIndices = int(timeBetweenWindows/timeBetweenSamples)
#padTimesPerWindow = nTimesPerWindow + gapTimeIndices
#nStackTimes = (endSlice-startSlice)*padTimesPerWindow
stackArr = np.zeros(((endSlice-startSlice)*nTimesPerWindow,nChannels)) #(nStackTimes,nChannels))
for sliceID in range(startSlice,endSlice):
	startID = nTimesPerWindow*(sliceID-startSlice) #padTimesPerWindow*(sliceID-startSlice)
	stackArr[startID:startID+nTimesPerWindow,:] = np.flipud(data[sliceID,:,:])
clip = np.percentile(np.absolute(stackArr),97)
#startTimeS = 0
#endTimeS = nStackTimes*timeBetweenSamples
#startLocM = location[0]
#endLocM = location[-1]
plt.imshow(stackArr,aspect='auto',interpolation='nearest',vmin=-clip,vmax=clip,cmap=plt.get_cmap('seismic')) # ,extent=(startLocM,endLocM,endTimeS,startTimeS)
plt.colorbar()
plt.ylabel('time (s) within windows')
plt.xlabel('location (m)')
plt.title('windows '+str(startSlice)+' to '+str(endSlice))
plt.savefig('fig/thirdTest' + exampleName)
plt.clf()

# show all data
startSlice = 0
endSlice =nWindows
#timeBetweenWindows = timing[startSlice+1,0]-timing[startSlice,-1]
#timeBetweenSamples = timing[startSlice,1]-timing[startSlice,0]
#gapTimeIndices = int(timeBetweenWindows/timeBetweenSamples)
#padTimesPerWindow = nTimesPerWindow + gapTimeIndices
#nStackTimes = (endSlice-startSlice)*padTimesPerWindow
stackArr = np.zeros((nWindows*nTimesPerWindow,nChannels)) #(nStackTimes,nChannels))
for sliceID in range(startSlice,endSlice):
	startID = nTimesPerWindow*(sliceID-startSlice) #padTimesPerWindow*(sliceID-startSlice)
	stackArr[startID:startID+nTimesPerWindow,:] = data[sliceID,:,:]
clip = np.percentile(np.absolute(stackArr),97)
#startTimeS = 0
#endTimeS = nStackTimes*timeBetweenSamples
#startLocM = location[0]
#endLocM = location[-1]
plt.imshow(stackArr,aspect='auto',interpolation='nearest',vmin=-clip,vmax=clip,cmap=plt.get_cmap('seismic')) # extent=(startLocM,endLocM,endTimeS,startTimeS),
plt.colorbar()
plt.ylabel('time (s) within windows') # relative to slice '+str(startSlice))
plt.xlabel('location (m)')
plt.title('windows '+str(startSlice)+' to '+str(endSlice))
plt.savefig('fig/fourthTest' + exampleName)
plt.clf()


