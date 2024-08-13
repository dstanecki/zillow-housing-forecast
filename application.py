from flask import Flask, render_template, request, flash
import mysql.connector
import mariadb

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')
    
@application.route('/process', methods =['GET', 'POST'])
@application.route('/process', methods=['GET', 'POST'])
def process():
    try:
        zip_code = request.form['zip']
        conn = mariadb.connect(host='mariadb', port=3306, user='root', password='password', database='ZillowHomeValueForecast')
        cur = conn.cursor()
        #cur.execute("SELECT `COL 2`, `COL 12` FROM `forecast` WHERE `COL 2`=%s", (zip_code,))
        #cur.execute("SELECT `2025-07-31` FROM forecast WHERE RegionName = %s", (zip_code))
        cur.execute("SELECT RegionName, `2025-07-31` FROM forecast WHERE RegionName=%s", (zip_code,))
        rows = cur.fetchall()
        if not rows:
            error = "No data found for the provided ZIP code."
            return render_template("index.html", error=error)
        return render_template("index.html", rows=rows)
    except mariadb.Error as e:
        return render_template("index.html", error=str(e))
    finally:
        cur.close()
        conn.close()

    
    
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host="0.0.0.0", port=5000)