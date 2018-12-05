# dynamicbusScheduling
Things to install:
1. MongoDb
2. NodeJS
3. Python

Folder Structure:

1. NodeJS: This folder has the dynamic bus scheduling algorithm in UIandAlgo.js file. Alexa development file can be found in routes/index.js. The web application files can be found in 'Views' folder. Rest of the files are for integration purposes.
2. Python_Code: This folder has script, 'travel_requests_simulator.py' to generate Poisson Distribution. This file is executed by running MainSim.py. The script generates travel requests based on poisson distribution and adds it into the mongoDB. 
3. database: This folder has all the JSON files used to create MongoDB collection. The 'conversion' folder has scripts written to reformat JSON files.
4. eval: This folder has poisson documents and graph generated after evaluation.

How to run:

Once the mongoDB collection is populated. Use following commands to run the algorithm and see the web application.
node UIandAlgo.js

Web application can be accessed from:
ec2domain:9999

To run Alexa Skill handler use:
node bin/www
