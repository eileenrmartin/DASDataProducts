import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
import scipy
import sys
plt.switch_backend('agg')
filename = '/content/drive/MyDrive/20201202_Kafadar/UTC-YMD20201202-HMS174339.516/Kafadar_Coupling_deformation_UTC-YMD20201202-HMS174339.516_seq_00000000000.hdf5'
#filename = sys.argv[1]

f = h5py.File(filename, 'r')

print(f.attrs.keys())

print(f.attrs['dT'])

print(list(f.keys()))

print(list(f['deformation'].keys()))

deform = f['deformation/frame_0000000000']
print(deform.shape)
print(deform.dtype)
print(deform.attrs['dT'])
print(deform.attrs['dx'])
print(deform.attrs['frame_id'])
print(deform.attrs['fver'])
print(deform.attrs['nT'])
print(deform.attrs['nx'])

print(deform.attrs.keys())


deform1 = f['deformation/frame_0000000001']
print(deform1.shape)
print(deform1.dtype)
print(deform1.attrs['dT'])
print(deform1.attrs['dx'])
print(deform1.attrs['frame_id'])
print(deform1.attrs['fver'])
print(deform1.attrs['nT'])
print(deform1.attrs['nx'])


clip = np.percentile(np.absolute(deform),85)
fig0 = plt.figure()
img0 = plt.imshow(deform, cmap='seismic', aspect='auto', interpolation='none')#, vmin=0, vmax=clip)
plt.ylabel('Time Sample')
plt.xlabel('Spacial point #')
plt.title('Deformation Frame 0')
plt.colorbar()
plt.show()



ndef = np.array(deform)
defft = np.abs(fft.rfft2(ndef, axes=-2))



clip = np.percentile(np.absolute(defft[:, :700]),85)
fig1 = plt.figure()
img1 = plt.imshow(defft[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.title('FFT of Deformation Frame 0')
plt.colorbar()
plt.show()



ndef2 = np.array(deform1)
defft2 = np.abs(fft.rfft2(ndef2, axes=-2))



clip = np.percentile(np.absolute(defft2[:, :700]),85)
fig2 = plt.figure()
img2 = plt.imshow(defft2[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.colorbar()
plt.show()



deform4 = f2['deformation/frame_0000000814']
ndef5 = np.array(deform4)
defft5 = np.abs(fft.rfft2(ndef5, axes=-2))

deform5 = f2['deformation/frame_0000000815']
ndef6 = np.array(deform5)
defft6 = np.abs(fft.rfft2(ndef6, axes=-2))




clip = np.percentile(np.absolute(defft5[:, :700]),85)
fig5 = plt.figure()
img5 = plt.imshow(defft5[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.colorbar()
plt.show()





clip = np.percentile(np.absolute(defft6[:, :700]),85)
fig6 = plt.figure()
img6 = plt.imshow(defft6[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.colorbar()
plt.show()





filename2 = '/content/drive/MyDrive/20201202_Kafadar/UTC-YMD20201202-HMS174339.516/Kafadar_Coupling_deformation_UTC-YMD20201202-HMS175010.762_seq_00000000003.hdf5'

f2 = h5py.File(filename, 'r')





deform2 = f2['deformation/frame_0000000000']
ndef3 = np.array(deform2)
defft3 = np.abs(fft.rfft2(ndef3, axes=-2))

deform3 = f2['deformation/frame_0000000001']
ndef4 = np.array(deform3)
defft4 = np.abs(fft.rfft2(ndef4, axes=-2))




clip = np.percentile(np.absolute(defft3[:, :700]),85)
fig3 = plt.figure()
img3 = plt.imshow(defft3[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.colorbar()
plt.show()




clip = np.percentile(np.absolute(defft4[:, :700]),85)
fig4 = plt.figure()
img4 = plt.imshow(defft4[:, :700], cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Frequency bin')
plt.xlabel('Spacial point #')
plt.colorbar()
plt.show()









deformframes = f['deformation/frame_'+str(0).zfill(10)][:,:]
for k in range(1,30):
    deformation_frame = f['deformation/frame_'+str(k).zfill(10)][:,:]
    deformframes = np.concatenate([deformframes, deformation_frame],axis=0)

clip = np.percentile(np.absolute(deformframes),95)
fig0 = plt.figure()
img0 = plt.imshow(deformframes, cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Time sample')
plt.xlabel('Spacial point #')
plt.title('Deformation Frames 0-29')
plt.colorbar()
plt.show()




#append together multiple frames to visually look for differences
deformframes2 = f2['deformation/frame_'+str(0).zfill(10)][:,:]
for k in range(1,30):
    deformation_frame = f2['deformation/frame_'+str(k).zfill(10)][:,:]
    deformframes2 = np.concatenate([deformframes2, deformation_frame],axis=0)

clip = np.percentile(np.absolute(deformframes2),95)
fig0 = plt.figure()
img0 = plt.imshow(deformframes2, cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Time sample')
plt.xlabel('Spacial point #')
plt.title('Deformation Frames 0-29')
plt.colorbar()
plt.show()




#npdeform = np.array(deform)
deformfft = np.abs(fft.rfft2(deformframes[:,:700], axes=-2))

clip = np.percentile(np.absolute(deformfft),90)
fig2 = plt.figure()
img2 = plt.imshow(deformfft, cmap='seismic', aspect='auto', interpolation='none', vmin=0, vmax=clip)
plt.ylabel('Freq bin')
plt.xlabel('Spacial point #')
plt.title('Deformation Frames 0-29')
plt.colorbar()
plt.show()


f.close()
f2.close()

