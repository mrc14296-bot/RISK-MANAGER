from flask import (
    Flask, render_template, request, session,
    jsonify, redirect, url_for, flash, Response
)
from flask_login import (
    LoginManager, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
from functools import wraps
import os, uuid, csv, io, hashlib, hmac

from models import db, User, SubscriptionHistory
import logic
import config
import razorpay

app = Flask(__name__)
app.secret_key = "trading_secret_key_ultra_secure_2025"

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False

# Constants
GRACE_DAYS = 3  # Added missing constant
RAZORPAY_MONTHLY_PLAN_ID = config.RAZORPAY_MONTHLY_PLAN_ID
RAZORPAY_YEARLY_PLAN_ID = config.RAZORPAY_YEARLY_PLAN_ID

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Google OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Razorpay Client Setup
razorpay_client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))

def get_month_end(dt=None):
    if not dt:
        dt = datetime.utcnow()
    next_month = dt.replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1) - timedelta(seconds=1)

# --- DECORATORS ---

def subscription_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

        if current_user.is_paused:
            flash("Subscription is paused. Contact admin.", "error")
            return redirect(url_for('home'))

        if not current_user.subscription_end:
            flash("No active subscription.", "warning")
            return redirect(url_for('subscribe'))

        now = datetime.utcnow()
        # grace_end uses the GRACE_DAYS constant defined above
        grace_end = current_user.subscription_end + timedelta(days=GRACE_DAYS)

        if now > grace_end:
            current_user.is_subscribed = False
            current_user.subscription_status = "expired"
            db.session.commit()
            flash("Subscription expired. Please renew.", "warning")
            return redirect(url_for('subscribe'))

        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access only", "error")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# --- ADMIN ROUTES ---

@app.route('/admin/pause/<int:user_id>')
@login_required
@admin_required
def pause_subscription(user_id):
    user = User.query.get_or_404(user_id)
    user.is_paused = True
    user.paused_at = datetime.utcnow()
    db.session.commit()
    flash("Subscription paused", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/resume/<int:user_id>')
@login_required
@admin_required
def resume_subscription(user_id):
    user = User.query.get_or_404(user_id)
    if user.paused_at:
        paused_duration = datetime.utcnow() - user.paused_at
        if user.subscription_end:
            user.subscription_end += paused_duration
    
    user.is_paused = False
    user.paused_at = None
    db.session.commit()
    flash("Subscription resumed", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin.html', users=users)

# --- PUBLIC PAGES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_alias():
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# --- AUTHENTICATION ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password", "error")
            return render_template('login.html')

        if user.active_session:
            flash("This account is already logged in. Please logout first.", "error")
            return redirect(url_for('login'))

        login_user(user)

        if not user.subscription_end:
            user.is_subscribed = True
            user.subscription_type = "trial"
            user.subscription_status = "active"
            user.subscription_start = datetime.utcnow()
            user.subscription_end = get_month_end()

        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        user.active_session = session_id
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/login/google')
def google_login():
    return google.authorize_redirect(url_for('google_authorize', _external=True))

@app.route('/authorize/google')
def google_authorize():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    user = User.query.filter_by(email=user_info['email']).first()

    if not user:
        user = User(
            username=user_info['name'],
            email=user_info['email'],
            google_id=user_info['sub']
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    if not user.subscription_end:
        user.is_subscribed = True
        user.subscription_type = "trial"
        user.subscription_status = "active"
        user.subscription_start = datetime.utcnow()
        user.subscription_end = get_month_end()
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    current_user.active_session = None
    db.session.commit()
    logout_user()
    session.pop('session_id', None)
    return redirect(url_for('login'))

# --- RAZORPAY ROUTES ---

@app.route('/subscribe')
@login_required
def subscribe():
    return render_template('subscribe.html', key_id=config.RAZORPAY_KEY_ID, user=current_user)

@app.route('/create-subscription', methods=['POST'])
@login_required
def create_subscription():
    try:
        data = request.get_json()
        plan_type = data.get("plan_type")
        plan_id = RAZORPAY_MONTHLY_PLAN_ID if plan_type == "monthly" else RAZORPAY_YEARLY_PLAN_ID
        
        subscription_data = {
            "plan_id": plan_id,
            "total_count": 12,
            "quantity": 1,
            "customer_notify": 1,
            "notes": {"user_id": current_user.id, "email": current_user.email}
        }
        subscription = razorpay_client.subscription.create(subscription_data)
        return jsonify({"success": True, "subscription_id": subscription["id"]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/verify-subscription', methods=['POST'])
@login_required
def verify_subscription():
    try:
        data = request.get_json()
        # Security Verification
        razorpay_client.utility.verify_subscription_payment_signature({
            "razorpay_payment_id": data.get("razorpay_payment_id"),
            "razorpay_subscription_id": data.get("razorpay_subscription_id"),
            "razorpay_signature": data.get("razorpay_signature")
        })

        sub_id = data.get("razorpay_subscription_id")
        # Fetch the subscription from Razorpay to see which plan it belongs to
        razorpay_sub = razorpay_client.subscription.fetch(sub_id)
        razorpay_plan_id = razorpay_sub.get('plan_id')

        if razorpay_plan_id == RAZORPAY_YEARLY_PLAN_ID:
            plan_type = "yearly"
        else:
            plan_type = "monthly"

        current_user.is_subscribed = True
        current_user.subscription_id = sub_id
        current_user.subscription_status = "active"
        current_user.subscription_type = plan_type
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = get_month_end()

        history = SubscriptionHistory(
            user_id=current_user.id,
            plan_type=plan_type,
            start_date=current_user.subscription_start,
            end_date=current_user.subscription_end,
            status="active"
        )
        db.session.add(history)
        db.session.commit()

        return jsonify({
            "success": True, 
            "plan": plan_type, 
            "valid_till": current_user.subscription_end.strftime("%Y-%m-%d")
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/check-subscription')
@login_required
def check_subscription():
    if current_user.is_subscribed:
        if current_user.subscription_end and current_user.subscription_end > datetime.utcnow():
            return jsonify({
                'subscribed': True,
                'status': current_user.subscription_status,
                'end_date': current_user.subscription_end.strftime('%Y-%m-%d')
            })
        else:
            current_user.subscription_status = 'expired'
            current_user.is_subscribed = False
            db.session.commit()
    return jsonify({'subscribed': False, 'status': current_user.subscription_status or 'inactive'})

@app.route('/razorpay/webhook', methods=['POST'])
def razorpay_webhook():
    payload = request.data
    signature = request.headers.get('X-Razorpay-Signature')
    expected_signature = hmac.new(
        bytes(config.RAZORPAY_WEBHOOK_SECRET, 'utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        return jsonify({"error": "Invalid signature"}), 400

    event = request.get_json()
    if event['event'] in ['subscription.charged', 'subscription.completed']:
        sub_id = event['payload']['subscription']['entity']['id']
        user = User.query.filter_by(subscription_id=sub_id).first()
        if user:
            if event['event'] == 'subscription.charged':
                user.subscription_status = "active"
                user.is_subscribed = True
                user.subscription_end = get_month_end()
            else:
                user.subscription_status = "expired"
                user.is_subscribed = False
            db.session.commit()
    return jsonify({"status": "ok"})

# --- TRADING ROUTES ---

@app.route("/get_live_price/<symbol>")
@login_required
@subscription_required
def live_price_api(symbol):
    price = logic.get_live_price(symbol)
    return jsonify({"price": price if price else 0})

@app.route("/get_open_positions")
@login_required
def get_open_positions_api():
    return jsonify({"positions": logic.get_open_positions()})

@app.route("/get_trade_history")
@login_required
def get_trade_history_api():
    return jsonify({"trades": logic.get_trade_history()})
@app.route("/index", methods=["GET", "POST"])
@login_required
@subscription_required
def index():
    # 1. Initialize data
    logic.initialize_session()
    symbols = logic.get_all_exchange_symbols()
    live_bal, live_margin = logic.get_live_balance()

    balance = live_bal or 0.0
    margin_used = live_margin or 0.0
    unutilized = max(balance - margin_used, 0.0)

    # 2. Handle Form Inputs
    selected_symbol = request.form.get("symbol", "BTCUSDT")
    side = request.form.get("side", "LONG")
    order_type = request.form.get("order_type", "MARKET")
    margin_mode = request.form.get("margin_mode", "ISOLATED")

    # Entry logic
    current_price = logic.get_live_price(selected_symbol)
    entry_val = request.form.get("entry")
    entry = float(entry_val) if entry_val and float(entry_val) > 0 else current_price

    sl_type = request.form.get("sl_type", "SL % Movement")
    sl_val = float(request.form.get("sl_value") or 0)

    tp1 = float(request.form.get("tp1") or 0)
    tp1_pct = float(request.form.get("tp1_pct") or 0)
    tp2 = float(request.form.get("tp2") or 0)

    # 3. Position Sizing
    sizing = logic.calculate_position_sizing(unutilized, entry, sl_type, sl_val)
    trade_status = session.pop("trade_status", None)

    # 4. Handle Order Placement
    if request.method == "POST" and "place_order" in request.form:
        if not sizing.get("error"):
            result = logic.execute_trade_action(
                balance, selected_symbol, side, entry, order_type, sl_type, sl_val, sizing,
                float(request.form.get("user_units") or 0), 
                float(request.form.get("user_lev") or 0),
                margin_mode, tp1, tp1_pct, tp2
            )
            session["trade_status"] = result
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        user=current_user,
        trade_status=trade_status,
        sizing=sizing,
        balance=round(balance, 2),
        unutilized=round(unutilized, 2),
        symbols=symbols,  # This list is now correctly populated
        selected_symbol=selected_symbol,
        default_entry=entry,
        default_sl_value=sl_val,
        default_sl_type=sl_type,
        default_side=side,
        order_type=order_type,
        margin_mode=margin_mode,
        tp1=tp1,
        tp1_pct=tp1_pct,
        tp2=tp2,
        today_stats=logic.get_today_stats()
    )

# Database initialization
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)