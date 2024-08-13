# zillow-housing-forecast
Python Flask Web Application

Prerequisites to run: Python, Flask

If you don't already have Flask installed, see this link for steps https://flask.palletsprojects.com/en/3.0.x/installation/

This web app accepts a ZIP code as user input and queries a database that has official Zillow data loaded into it. It returns the one-year housing forecast in estimated percent-change for that ZIP code. 
More info here: https://danielstanecki.com/projects/2022/01/10/zillow-webapp.html

# docker build -t zhf .

# docker run -p 5000:5000 --detach 'zhf'