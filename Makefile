downloadVirtualTrebleServer:
	#Download wheel (This example uses python 3.8)
		#For python 3.6 use "cp36" before _v3.whl
		#For python 3.7 use "cp37" before _v3.whl
		#For python 3.8 use "cp38" before _v3.whl
	wget terra15.com.au/download/latestlinuxapi_cp38_v3.whl --content-disposition
	pip install acq_server-3.16.3-cp38-cp38-linux_x86_64.whl


#Setup T15 Acquisition server - Not working
setupT15Server:
	python SourceCode/T15/ServerSetup.py
