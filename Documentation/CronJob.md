## Using Cronjob

Cron is a background program for scheduling job submissions at specific times. Since data needs to be continuously fetched from the data stream every so often to 
calculate data products, cron jobs can be scheduled to run at intervals like every few minutes. This doc goes over the steps to start and check if cron is running 
and set up cron jobs to save data product files. (Note: any changes or edits to the parameter file should be done before scheduling jobs, and make sure the path to 
save the data product files to is correct in the parameter file)

### Checking Python Script

Open the terminal for the Linux system by clicking on the windows start button and searching for “terminal”. 
Click on the app.
Navigate into the “DASDataProducts” folder by typing 
'''plaintext 
cd
''' 
then a space, followed by the path to the folder. The path to the folder is the same location as the folder 
that would be followed using the File Explorer. For example, the location in this example system is in the user’s (“saman”) Documents, so the command is 
“cd Documents/DASDataProducts”. The location name on the left of the blinking cursor should now display the location of the folder and its name. 
 
Navigate into the SourceCode folder by typing “cd SourceCode”. The files in the directory can be listed with the command “ls -l”. Make sure the file save_data_prod.py is executable by typing the command “chmod +x save_data_prod.py”. 
To make sure the save_data_prod.py script can be called by cron, the line endings must be changed in the file from Windows format to Unix format. First the package dos2unix must be installed by typing “sudo apt install dos2unix”. Then, type the administrator password and hit enter. 
 
After the package is successfully installed, type the command ”dos2unix save_data_prod.py”. The terminal should state the file is being converted with the following message:
 

Finding file paths

To determine the full paths to the files needed for the cron job command, type “realpath save_data_prod.py”. Then type “realpath “ and the name of the parameter file that will be used, in this case named param.py. Copy those paths for adding into the crontab file next. 
 
 

Creating and editing crontab file

To create the crontab file that will contain the time to submit the jobs and what commands to run, type the command “crontab -e”. If a crontab has not already been created, the user must select an editor. Select “/bin/nano” by entering the corresponding number. 
 
The crontab file will then open. The crontab file heading explains the setup of the cron command. 
 
To type the command that will call the python script every minute, move the cursor to a line under the last line of the header, then type “* * * * * “ then the path to the save_data_prod.py file, then space and the path to the python parameter file to use. For example, the command for this example would be “* * * * * /mnt/c/Users/saman/Documents/DASDataProducts/SourceCode/save_data_prod.py /mnt/c/Users/saman/Documents/DASDataProducts/SourceCode/params.py”. 
 
Exit the crontab file by typing ctrl + x and type y to save the new file. Then hit enter to accept the file name. The terminal should display “crontab: installing new crontab”. The contents of the file can also be viewed from the terminal by typing the command “crontab -l”.
If the crontab file needed to be edited, the same file can be accessed by again typing “crontab -e”. If the time interval needs to be changed, for example have the script run every five minutes as opposed to every minute, the “* * * * *” should be changed to “*/5 * * * *”. 

Starting cron

To check the status of cron, type the command “service crond status” for Linux systems or “service cron status” for Debian systems (Ubuntu). To start cron if it is not running, type “service crond start” or “service cron start”. If the user does not have permissions (a message may display stating “cron: can't open or create /var/run/crond.pid: Permission denied” or “[fail]”), use the command “sudo service crond start” or “sudo service cron start”, then type the admin password and enter. Now when checking status, the command to check status should display that cron is running. 

Stopping cronjob

To stop the cron program, type “service crond stop” or “service cron stop”. If permissions are denied, add “sudo “ to the beginning of the command and enter the admin password. The specific command to run the save_data_prod.py script can also be commented out in the crontab file by editing it and adding “#” to the beginning of the line. 
