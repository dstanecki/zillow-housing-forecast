from flask import Flask, render_template, request, flash
import mysql.connector
import mariadb

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/process', methods=['GET', 'POST'])
def process():
    conn = None
    cur = None
    try:
        zip_code = request.form['zip']
        # Establish the database connection
        conn = mariadb.connect(
            host='mariadb',
            port=3306,
            user='root',
            password='password',
            database='ZillowHomeValueForecast'
        )
        cur = conn.cursor()
        # Execute the query
        cur.execute("SELECT RegionName, `2026-05-31` FROM forecast WHERE RegionName=%s", (zip_code,))
        rows = cur.fetchall()
        if not rows:
            error = "No data found for the provided ZIP code."
            return render_template("index.html", error=error)
        return render_template("index.html", rows=rows)
    except mariadb.Error as e:
        # Handle database errors
        return render_template("index.html", error=str(e))
    finally:
        # Close the cursor and connection if they were initialized
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Run the app
if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port=5000)
