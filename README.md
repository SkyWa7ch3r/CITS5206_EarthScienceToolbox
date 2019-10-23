# The Earth Science Toolbox
The aim of this project is to create a dashboard for a user without Python or terminal experience create publication quality plots.
It will be primarily focused on data coming from environmental data, however could in theory be used for all types of different projects. It will currently be based on Plotly and Dash.

To run the project please refer to the installation guide we have made. You could run the start.cmd from here in Windows which will create a virtual environment, install the necessary python packages and run the server.

To do this yourself apply the following commands
1. Create Virtual environment

To create a virtual environment with name mytoolbox
 python -m venv mytoolbox

2. Activate the Virtual environment

To activate a virtual environment mytoolbox
 .\env\Scripts\activate

3. Loading the packages Virtual environment

To load the required packages, the provided requirements.txt file containing all packages and dependencies should be placed in the same directory as the main toolbox application and run the following commands
 
 pip install -r requirements.txt

4. To run the application run the following commands
 python toolbox.py


