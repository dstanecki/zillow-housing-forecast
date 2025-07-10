from flask import Flask, session, render_template, request
import mariadb
import os
import requests
import redis
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from openai import AzureOpenAI
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

# reCAPTCHA
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")

# Redis Cache credentials
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

REDIS_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

# Flask rate limiter (per-client, Layer 7)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URI,
    app=app,
)

# Connect to Redis to cache AI responses
redis_client = redis.StrictRedis.from_url(REDIS_URI, decode_responses=True)

def verify_recaptcha(token):
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }
    try:
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        return r.json().get("success", False)
    except:
        return False

@app.route('/')
def index():
    return render_template("index.html", rows=session.get('results', []), recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.route('/process', methods=['GET', 'POST'])
@limiter.limit("6 per minute")
def process():
    forecast_requests_total.inc()

    conn = None
    cur = None
    try:
        zip_code = request.form['zip']
        
        # Enforce session cap
        if 'results' in session and len(session['results']) >= 10:
            error = "Result limit reached. Please clear results before submitting more queries."
            return render_template("index.html", rows=session['results'], error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)

        # First-time users must solve reCAPTCHA
        if not session.get('captcha_passed'):
            token = request.form.get('g-recaptcha-response')
            if not verify_recaptcha(token):
                error = "reCAPTCHA verification failed. Please try again."
                return render_template("index.html", rows=session.get('results', []), error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)
            session.permanent = False  # expires on browser close
            session['captcha_passed'] = True

        # Connect to MariaDB
        conn = mariadb.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            port=3306,
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ZillowHomeValueForecast")
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT RegionName, `2026-05-31`, StateName, City, Metro, CountyName, BaseDate FROM forecast WHERE RegionName=%s",
            (zip_code,)
        )
        rows = cur.fetchall()

        if not rows:
            error = "No data found for the provided ZIP code."
            return render_template("index.html", rows=session.get('results', []), error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)

        # Extract values
        forecast = rows[0][1]
        state = rows[0][2]
        city = rows[0][3]
        metro = rows[0][4]
        county = rows[0][5]
        baseDate = rows[0][6]

        # Prompt for Azure AI
        user_prompt = (
            f"Home values in ZIP code {zip_code} are forecasted to change by {forecast}% from {baseDate} to one year later. "
            f"This area includes {city}, {state}, within the {metro} metro and {county}. "
            f"In a short paragraph, give a concise explanation (2–3 key reasons) why this change is expected, based on local housing or economic trends specific to this region."
        )

        # Check to see if AI explanation is in Redis Cache already
        cache_key = f"explanation:{zip_code}"
        cached_explanation = redis_client.get(cache_key)

        if cached_explanation:
            explanation = cached_explanation
        else:
            # Call Azure OpenAI
            try:
                response = client.chat.completions.create(
                    model="o4-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a real estate analyst who specializes in regional housing trends. Your answers are short but highly specific to the ZIP code, city, and regional context given. Avoid repeating generic causes like 'interest rates' unless clearly relevant."
                        },
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                explanation = response.choices[0].message.content
                # Cache explanation for 30 days
                redis_client.setex(cache_key, 2592000, explanation)     
            except Exception as e:
                explanation = f"(AI explanation unavailable: {str(e)})"

        # Store result
        result_rows = [(zip_code, forecast, explanation)]
        if 'results' not in session:
            session['results'] = []
        session['results'] = result_rows + session['results']

        return render_template("index.html", rows=session['results'], recaptcha_site_key=RECAPTCHA_SITE_KEY)

    except mariadb.Error as e:
        return render_template("index.html", rows=session.get('results', []), error=str(e), recaptcha_site_key=RECAPTCHA_SITE_KEY)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/clear', methods=['GET'])
def clear():
    session.pop('results', None)
    session.pop('captcha_passed', None)
    return render_template("index.html", rows=[], recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("index.html", rows=session.get('results', []), error="Rate limit exceeded. Please wait a moment and try again."), 429

# Metrics
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
