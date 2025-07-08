from flask import Flask, session, render_template, request
import mariadb
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from openai import AzureOpenAI

# Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://zhf-agent-resource.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
    api_key=os.getenv("SUBSCRIPTION_KEY", "")
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
forecast_requests_total = Counter('forecast_request_total', 'Total number of forecast ZIP code queries')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    forecast_requests_total.inc()

    conn = None
    cur = None
    try:
        zip_code = request.form['zip']

        # Connect to MariaDB
        conn = mariadb.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            port=3306,
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ZillowHomeValueForecast")
        )
        cur = conn.cursor()
        cur.execute("SELECT RegionName, `2026-05-31`, StateName, City FROM forecast WHERE RegionName=%s", (zip_code,))
        rows = cur.fetchall()

        if not rows:
            error = "No data found for the provided ZIP code."
            return render_template("index.html", rows=session.get('results', []), error=error)

        # Get values
        forecast = rows[0][1]
        state = rows[0][2]
        city = rows[0][3]

        # Build GPT prompt
        user_prompt = (
            f"ZIP code {zip_code} is forecasted to change by {forecast}% over the next year. "
            f"In less than 3 sentences, mention that the zip code is located in {city}, {state} and decisively give 2–3 reasons why this is happening."
        )

        # Call Azure OpenAI for explanation
        explanation = ""
        try:
            response = client.chat.completions.create(
                model="o4-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that confidently explains real estate market trends clearly."},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            explanation = response.choices[0].message.content
        except Exception as e:
            explanation = f"(AI explanation unavailable: {str(e)})"

        # Format result for table: (zip, forecast, explanation)
        result_rows = [(zip_code, forecast, explanation)]

        # Add to session history
        if 'results' not in session:
            session['results'] = []
        session['results'] = result_rows + session['results']

        return render_template("index.html", rows=session['results'])

    except mariadb.Error as e:
        return render_template("index.html", rows=session.get('results', []), error=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/clear', methods=['GET'])
def clear():
    session.pop('results', None)
    return render_template("index.html", rows=[])

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
