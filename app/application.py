from flask import Flask, render_template, request, flash
import mysql.connector
import mariadb
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)

# Expose /metrics
metrics = PrometheusMetrics(app)
print("Prometheus metrics initialized")

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Custom Prometheus counter
forecast_requests_total = Counter('forecast_request_total', 'Total number of forecast ZIP code queries')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    # Increment metric
    forecast_requests_total.inc()

    conn = None
    cur = None
    try:
        zip_code = request.form['zip']
        # Establish the database connection using env vars defined in app-deployment.yaml with fallback defaults
        conn = mariadb.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            port=3306,
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ZillowHomeValueForecast")
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

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# Run the app
if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
