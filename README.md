## GRID 3.0 Competition Participation Repository

This is a repository having all the code i wrote to attempt to finish the tasks given in the Flipkart Grid 3.0 competition - Robotics division.

The task specs are given in the **taskspecs** folder, if you wish to know more

There is a project report pdf - **Flipkart Project Report** conceptually explaining the preliminary task and the path i followed to complete it. However, this only contains details of prototype-1 of the project, which doesn't use aruco markers or the A* search algorithm. It should help you get an understanding of the approach and what all this code means, however.

## Different Sections:

### assets:
- it contains the map, images i used to test and configure my code properly, some of the csv files and other stuff that was relevant to the task

### buildingblocks:
- **botfinders** has the code files i wrote to scan an image and accurately find the position and orientation of a bot, either based on 2 differently sized colored markers, or aruco markers
- **carcontrol** has the code files i wrote to control the bot using a local router connected and udp transmission that was picked up by my nodeMCUs connected to bots
- **mapmakers** has the code that uses opencv to digitize the physical map that the bots are supposed to move on for computer understanding and logic application
- **videotesters** are the files used to test the video feed and look for any errors, false positives, or missed negatives
- **readPackageList** is a basic file to read the csv file of the task
- **threadingtest** is a practice file that i coded to learn and implement parallel computing using the "threading" library in python

### mains:
- this has all the attempts of a **main.py** i coded. All main files have different versions of the buildingblock files used in them.
- The main files were the final code that ran the project tasks and they use at least a version of all the building blocks somewhere in the code

### Arduino-NodeMCU-code
- this folder has all the robot-side, arduino and NodeMCU code, written in c++. 