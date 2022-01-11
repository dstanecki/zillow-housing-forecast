from flask import Flask, render_template, request, flash
import mysql.connector
import mariadb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/process', methods =['GET', 'POST'])
def process():
    zip = request.form['zip'] #takes ZIP code value from HTML POST form
    conn = mariadb.connect(host='IP', port= 3306, user='user', password='password', database='ZillowHomeValueForecast')
    cur = conn.cursor()
    cur.execute("SELECT `COL 2`, `COL 7` FROM `forecast` WHERE `COL 2`=%s", (zip,)) #lists columns 2 and 7 which are ZIP code and 1-yr percent home value change respectively... where the entered ZIP matches a row in column 2
    rows = cur.fetchall()
    return render_template("index.html", rows = rows)
    
    
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()