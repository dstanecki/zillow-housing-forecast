from flask import Flask, session, render_template, request, redirect, url_for, g
import mariadb
import os
import requests
import redis
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from openai import AzureOpenAI
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token

# Initialize Azure OpenAI client for generating regional housing explanations
# The endpoint and API key are read from environment variables for security
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://zhf-agent-resource.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",
    api_key=os.getenv("SUBSCRIPTION_KEY", "")
)

app = Flask(__name__)
# Session key to sign cookies (must be kept secret in production)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# OAuth credentials
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Configure Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
forecast_requests_total = Counter('forecast_request_total', 'Total number of forecast ZIP code queries')

# reCAPTCHA credentials
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")

# Redis credentials for caching AI responses and storing rate-limiter data
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

# Rate limiter configured to use Redis storage (Layer 7 protection)
# Limits requests per client IP to prevent abuse
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URI,
    app=app,
)

# Redis client for caching AI explanations to reduce cost/latency
redis_client = redis.StrictRedis.from_url(REDIS_URI, decode_responses=True)

@app.before_request
def load_user():
    g.user = session.get("user")

@app.route("/login")
def login():
    nonce = generate_token(24)
    session["oidc_nonce"] = nonce
    REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "https://zhf.danielstanecki.com/login/callback")
    google = oauth.create_client('google')
    return google.authorize_redirect(REDIRECT_URI, nonce=nonce)

@app.route("/login/callback")
def auth_callback():
    token = google.authorize_access_token()
    nonce = session.pop("oidc_nonce", None)
    userinfo = google.parse_id_token(token, nonce=nonce)  # verified OIDC claims
    # store the minimal fields you need
    session["user"] = {
        "sub": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture"),
    }
    # optional: set session.permanent, etc.
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    
def verify_recaptcha(token):
    """
    Verify a reCAPTCHA token with Google’s API.
    Returns True if valid, False otherwise.
    """
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }
    try:
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        return r.json().get("success", False)
    except:
        # Fail closed if verification request fails
        return False

@app.route('/')
def index():
    """
    Render main page with previous results (if any) and reCAPTCHA key.
    """
    return render_template("index.html", rows=session.get('results', []), recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.route('/process', methods=['GET', 'POST'])
@limiter.limit("6 per minute") # enforce per-IP request rate limiting
def process():
    """
    Handle user ZIP code queries:
    - Validate reCAPTCHA for new users
    - Fetch forecast data from MariaDB
    - Generate/cache AI explanation via Azure OpenAI
    - Store results in session for persistence across requests
    """
    forecast_requests_total.inc()

    conn = None
    cur = None
    try:
        zip_code = request.form['zip']
        
        # Enforce per-session query cap (prevents excessive storage in cookies)
        if 'results' in session and len(session['results']) >= 10:
            error = "Result limit reached. Please clear results before submitting more queries."
            return render_template("index.html", rows=session['results'], error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)

        # Require CAPTCHA for first-time users to mitigate bot submissions
        if not session.get('captcha_passed'):
            token = request.form.get('g-recaptcha-response')
            if not verify_recaptcha(token):
                error = "reCAPTCHA verification failed. Please try again."
                return render_template("index.html", rows=session.get('results', []), error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)
            session.permanent = False  # expires on browser close
            session['captcha_passed'] = True

        # Connect to MariaDB and query forecasts for given ZIP code
        conn = mariadb.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            port=3306,
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ZillowHomeValueForecast")
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT RegionName, YearForecast, StateName, City, Metro, CountyName, BaseDate FROM forecast WHERE RegionName=%s",
            (zip_code,)
        )
        rows = cur.fetchall()

        if not rows:
            # No forecast data found for the provided ZIP
            error = "No data found for the provided ZIP code."
            return render_template("index.html", rows=session.get('results', []), error=error, recaptcha_site_key=RECAPTCHA_SITE_KEY)

        # Extract database fields into named variables
        forecast = rows[0][1]
        state = rows[0][2]
        city = rows[0][3]
        metro = rows[0][4]
        county = rows[0][5]
        baseDate = rows[0][6]

        # Construct prompt for Azure AI model
        user_prompt = (
            f"Home values in ZIP code {zip_code} are forecasted to change by {forecast}% from {baseDate} to one year later. "
            f"This area includes {city}, {state}, within the {metro} metro and {county}. "
            f"In a short paragraph, give a concise explanation (2–3 key reasons) why this change is expected, based on local housing or economic trends specific to this region."
        )

        # Check Redis cache for previously generated explanation
        cache_key = f"explanation:{zip_code}"
        cached_explanation = redis_client.get(cache_key)

        if cached_explanation:
            explanation = cached_explanation
        else:
            # Call Azure OpenAI to generate explanation if not cached
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
                # Cache AI explanation for 30 days (2592000 seconds)
                redis_client.setex(cache_key, 2592000, explanation)     
            except Exception as e:
                # Gracefully handle AI errors by embedding error text
                explanation = f"(AI explanation unavailable: {str(e)})"

        # Store result at the top of session history
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
    """
    Clear session results and captcha state (reset workflow).
    """
    session.pop('results', None)
    session.pop('captcha_passed', None)
    return render_template("index.html", rows=[], recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.route('/ready')
def readiness_probe():
    """
    Readiness probe for Kubernetes/health checks.
    Returns HTTP 200 when app is up.
    """
    return 'OK', 200

@app.errorhandler(429)
def ratelimit_handler(e):
    """
    Custom handler for rate-limit violations (HTTP 429).
    Returns a friendly error page instead of default response.
    """
    return render_template("index.html", rows=session.get('results', []), error="Rate limit exceeded. Please wait a moment and try again."), 429

# Register a Prometheus counter that tracks requests per path
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == "__main__":
    # Run in production mode (debug off)
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
