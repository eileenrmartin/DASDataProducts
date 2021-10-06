#Runs low pass example with equation specified in file.
runEx:
	rm -f figures/lowpassFigure.png
	rm -f figures/lowpassFigureDownsampled.png
	rm -f figures/ampSpectrum.png
	rm -f figures/ampSpectrumDownsampled.png
	rm -f figures/logAmpSpectrum.png
	rm -f figures/logAmpSpectrumDownsampled.png
	python3 lowpassAndDownsampleEx.py
	
runTiming:
	python3 lowpassAndDownsampleTimingEx.py
runFileEx:	
	rm -f figures/lowpassFigure.png
	rm -f figures/lowpassFigureDownsampled.png
	rm -f figures/ampSpectrum.png
	rm -f figures/ampSpectrumDownsampled.png
	rm -f figures/logAmpSpectrum.png
	rm -f figures/logAmpSpectrumDownsampled.png
	python3 lowpassAndDownsampleFileEx.py /projects/permafrost/UTC-YMD20210909-HMS181615.358/AK_strain_rate_UTC-YMD20210909-HMS182034.642_seq_00000000002.hdf5
#/projects/permafrost/UTC-YMD20210908-HMS200646.050/AK_strain_rate_UTC-YMD20210908-HMS200646.050_seq_00000000000.hdf5


runRasterEx:	
	rm -f figures/rasterPlot.png
	python3 rasterPlotFileEx.py /projects/permafrost/UTC-YMD20210909-HMS181615.358/AK_strain_rate_UTC-YMD20210909-HMS182034.642_seq_00000000002.hdf5
