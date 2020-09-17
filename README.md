# Data-Visualization-App  
  
A native application that can visualize sensor data. The time-series data are given in XML file format and are stored
in a local database. The user can interact with the app via a GUI made with Qt and can choose a variety of charts in 
order to visualize the data over specified time periods.

---

## Setup  

Firstly, clone this repo:  
  
`git clone https://github.com/theokont/Data-Visualization-App`  
  
Then create a Python virtual environment and activate it:  
  
`cd Data-Visualization-App` -> `python3 -m venv venv`  
  
Activation:  
  
**Linux/MacOS** : `./venv/bin/activate` | **Windows** : `./venv/Scripts/activate.bat`  

After that comes the installation of the required libraries:  
  
`pip install -r requirements.txt`  
  
## Requirements  
  
**Data entry**  

This app had to accept multiple XML files where each of them had the following tags:  

`<UNIT> </UNIT>`  -> unit type  
`<VALUE> </VALUE>` -> value  
`<TIME> </TIME>`  -> timestamp  

While parsing the xml files, the program searches for these three tags, so they must be included in the XML Schema  

<**TIME**>  
  
The timestamp must be represented in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. This is essential in
 order to convert datetime strings to datetime objects. An example of ISO 8601 format:  
 
`YYYY-MM-DDTHH:MM:SS.ffffffZ`  
 
## Run the app  
  
`python 3 app.py`  
  
By running the app, the Qt GUI will pop.   
  



   

