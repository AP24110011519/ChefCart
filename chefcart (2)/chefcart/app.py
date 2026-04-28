"""
ChefCart – Smart Chef Booking Platform
=======================================
Backend: Flask + Python built-in sqlite3
No external DB library needed beyond Flask itself.
"""

from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import sqlite3, os

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "chefcart_secret_key_2024"   # Change in production!

DB_PATH = os.path.join(os.path.dirname(__file__), "chefcart.db")


# ── DB Helpers ────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query(sql, params=(), one=False):
    conn = get_db()
    cur  = conn.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    conn = get_db()
    cur  = conn.execute(sql, params)
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last


# ── Database Setup & Seed ─────────────────────────────────────────────────────
def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS user (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chef (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            cuisine    TEXT    NOT NULL,
            experience INTEGER NOT NULL,
            price      REAL    NOT NULL,
            bio        TEXT    DEFAULT '',
            photo_url  TEXT    DEFAULT '',
            email      TEXT    DEFAULT '',
            phone      TEXT    DEFAULT '',
            restaurant TEXT    DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS booking (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL REFERENCES user(id),
            chef_id    INTEGER NOT NULL REFERENCES chef(id),
            date       TEXT    NOT NULL,
            time_slot  TEXT    NOT NULL,
            status     TEXT    DEFAULT 'Confirmed',
            created_at TEXT    DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS review (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER REFERENCES user(id),
            chef_id    INTEGER NOT NULL REFERENCES chef(id),
            rating     INTEGER NOT NULL,
            comment    TEXT    DEFAULT '',
            created_at TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    _ensure_chef_columns(conn)
    conn.close()
    _seed_chefs()


def _ensure_chef_columns(conn):
    existing = [row[1] for row in conn.execute("PRAGMA table_info(chef)")]
    columns = [
        ("email", "TEXT DEFAULT ''"),
        ("phone", "TEXT DEFAULT ''"),
        ("restaurant", "TEXT DEFAULT ''"),
    ]
    for name, definition in columns:
        if name not in existing:
            conn.execute(f"ALTER TABLE chef ADD COLUMN {name} {definition}")


def _seed_chefs():
    if query("SELECT 1 FROM chef LIMIT 1", one=True):
        _seed_chef_contacts()
        return

    chefs = [
        ("Arjun Mehta",    "North Indian", 12, 2500,
         "Master of rich curries and tandoor delicacies. Trained in Delhi's finest kitchens.",
         "https://randomuser.me/api/portraits/men/32.jpg",
         "arjun.mehta@chefcart.com", "+91-9876501122", "Delhi Spice Den"),
        ("Priya Nair",     "South Indian",  8, 2000,
         "Expert in authentic Kerala and Tamil cuisine. Specialises in seafood and dosas.",
         "https://randomuser.me/api/portraits/women/44.jpg",
         "priya.nair@chefcart.com", "+91-9845012345", "Coconut Grove Kitchens"),
        ("Rahul Sharma",   "Chinese",       10, 2200,
         "Indo-Chinese fusion specialist with 5 years in Kolkata's Chinatown kitchens.",
         "https://randomuser.me/api/portraits/men/46.jpg",
         "rahul.sharma@chefcart.com", "+91-9900112233", "Dragon Wok Studio"),
        ("Sunita Reddy",   "Continental",   15, 3500,
         "European culinary graduate. Crafts exquisite pasta, risotto and continental classics.",
         "https://randomuser.me/api/portraits/women/68.jpg",
         "sunita.reddy@chefcart.com", "+91-9811223344", "The Continental Table"),
        ("Vikram Patel",   "Mughlai",        9, 2800,
         "Biryani and kebab maestro known for slow-cooked dum dishes and royal flavours.",
         "https://randomuser.me/api/portraits/men/55.jpg",
         "vikram.patel@chefcart.com", "+91-9876543214", "Nawab's Kitchen Hyderabad"),
        ("Ananya Singh",   "Italian",        7, 3000,
         "Pizza and pasta perfectionist trained in Rome. Brings authentic Italian warmth.",
         "https://randomuser.me/api/portraits/women/26.jpg",
         "ananya.singh@chefcart.com", "+91-9988776655", "La Piazza"),
        ("Kiran Desai",    "Mexican",        6, 1800,
         "Bold Mexican street food expert. Makes the best tacos this side of the border.",
         "https://randomuser.me/api/portraits/men/71.jpg",
         "kiran.desai@chefcart.com", "+91-9765432109", "Cantina Calle"),
        ("Meena Krishnan", "South Indian",  14, 2300,
         "Iyer household recipes passed through generations — authentic rasam and sambar.",
         "https://randomuser.me/api/portraits/women/52.jpg",
         "meena.krishnan@chefcart.com", "+91-9444012345", "Madras Spice House"),
        ("Rajan Iyer",     "North Indian",  11, 2600,
         "Punjabi dhaba style to fine dining — specialises in breads and gravies.",
         "https://randomuser.me/api/portraits/men/85.jpg",
         "rajan.iyer@chefcart.com", "+91-9911223344", "Punjab Swaad"),
        ("Fatima Sheikh",  "Mughlai",       13, 3200,
         "Hyderabadi dum biryani expert with Nawabi family recipes from the Nizam era.",
         "https://randomuser.me/api/portraits/women/79.jpg",
         "fatima.sheikh@chefcart.com", "+91-9870012345", "Royal Dum Biryani"),
    ]
    conn = get_db()
    conn.executemany(
        "INSERT INTO chef (name,cuisine,experience,price,bio,photo_url,email,phone,restaurant) VALUES (?,?,?,?,?,?,?,?,?)",
        chefs
    )
    reviews = [
        (None, 1, 5, "Absolutely divine curries!"),
        (None, 1, 4, "Very professional and tasty food."),
        (None, 2, 5, "Best dosas I have ever had!"),
        (None, 3, 4, "Great Manchurian and fried rice."),
        (None, 4, 5, "Continental feast — worth every rupee."),
        (None, 5, 5, "The biryani was out of this world."),
        (None, 5, 5, "Absolutely loved the kebabs."),
        (None, 6, 4, "Creamy pasta, authentic taste."),
        (None, 7, 4, "Fun experience, tacos were epic."),
        (None, 8, 5, "Grandma-style cooking, so comforting."),
        (None, 9, 4, "Dal makhani was chef's kiss."),
        (None, 10, 5, "Hyderabadi biryani was legendary."),
        (None, 10, 4, "Wonderful Nawabi experience."),
    ]
    conn.executemany(
        "INSERT INTO review (user_id,chef_id,rating,comment) VALUES (?,?,?,?)",
        reviews
    )
    conn.commit()
    conn.close()


def _seed_chef_contacts():
    contacts = {
        "Arjun Mehta":    ("arjun.mehta@chefcart.com", "+91-9876501122", "Delhi Spice Den"),
        "Priya Nair":     ("priya.nair@chefcart.com", "+91-9845012345", "Coconut Grove Kitchens"),
        "Rahul Sharma":   ("rahul.sharma@chefcart.com", "+91-9900112233", "Dragon Wok Studio"),
        "Sunita Reddy":   ("sunita.reddy@chefcart.com", "+91-9811223344", "The Continental Table"),
        "Vikram Patel":   ("vikram.patel@chefcart.com", "+91-9876543214", "Nawab's Kitchen Hyderabad"),
        "Ananya Singh":   ("ananya.singh@chefcart.com", "+91-9988776655", "La Piazza"),
        "Kiran Desai":    ("kiran.desai@chefcart.com", "+91-9765432109", "Cantina Calle"),
        "Meena Krishnan": ("meena.krishnan@chefcart.com", "+91-9444012345", "Madras Spice House"),
        "Rajan Iyer":     ("rajan.iyer@chefcart.com", "+91-9911223344", "Punjab Swaad"),
        "Fatima Sheikh":  ("fatima.sheikh@chefcart.com", "+91-9870012345", "Royal Dum Biryani"),
    }
    for name, (email, phone, restaurant) in contacts.items():
        execute(
            "UPDATE chef SET email=?, phone=?, restaurant=? WHERE name=?",
            (email, phone, restaurant, name)
        )


# ── Chef Helper ───────────────────────────────────────────────────────────────
def enrich_chef(chef):
    c = dict(chef)
    reviews = query("SELECT rating FROM review WHERE chef_id=?", (c["id"],))
    c["review_count"] = len(reviews)
    c["avg_rating"]   = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else 0.0
    return c


# ── Auth Decorator ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    all_chefs = [enrich_chef(c) for c in query("SELECT * FROM chef")]
    top_chefs = sorted(all_chefs, key=lambda c: c["avg_rating"], reverse=True)[:6]
    cuisines  = sorted(set(c["cuisine"] for c in all_chefs))
    return render_template("index.html", top_chefs=top_chefs, cuisines=cuisines)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name  = request.form.get("name",  "").strip()
        email = request.form.get("email", "").strip().lower()
        pwd   = request.form.get("password", "")
        if not name or not email or not pwd:
            flash("All fields are required.", "danger")
            return redirect(url_for("signup"))
        if query("SELECT id FROM user WHERE email=?", (email,), one=True):
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("login"))
        execute("INSERT INTO user (name,email,password) VALUES (?,?,?)",
                (name, email, generate_password_hash(pwd)))
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pwd   = request.form.get("password", "")
        if not email or not pwd:
            flash("Email and password are required.", "danger")
            return redirect(url_for("login"))
        user = query("SELECT * FROM user WHERE email=?", (email,), one=True)
        if not user or not check_password_hash(user["password"], pwd):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))
        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/chefs")
def chefs():
    cuisine    = request.args.get("cuisine",    "")
    min_price  = request.args.get("min_price",  type=float, default=0)
    max_price  = request.args.get("max_price",  type=float, default=999999)
    min_rating = request.args.get("min_rating", type=float, default=0)
    all_chefs  = [enrich_chef(c) for c in query("SELECT * FROM chef")]
    cuisines   = sorted(set(c["cuisine"] for c in all_chefs))
    filtered   = [
        c for c in all_chefs
        if (not cuisine or c["cuisine"] == cuisine)
        and (min_price <= c["price"] <= max_price)
        and (c["avg_rating"] >= min_rating)
    ]
    filtered.sort(key=lambda c: c["avg_rating"], reverse=True)
    return render_template("chefs.html", chefs=filtered, cuisines=cuisines,
                           selected_cuisine=cuisine, min_price=min_price,
                           max_price=max_price, min_rating=min_rating)


@app.route("/chef/<int:chef_id>")
def chef_detail(chef_id):
    raw = query("SELECT * FROM chef WHERE id=?", (chef_id,), one=True)
    if not raw:
        flash("Chef not found.", "danger")
        return redirect(url_for("chefs"))
    chef = enrich_chef(raw)
    reviews = query("""
        SELECT r.*, u.name AS user_name
        FROM review r
        LEFT JOIN user u ON u.id = r.user_id
        WHERE r.chef_id=?
        ORDER BY r.created_at DESC
    """, (chef_id,))
    suggestions = [enrich_chef(s) for s in
                   query("SELECT * FROM chef WHERE cuisine=? AND id!=? LIMIT 3",
                         (chef["cuisine"], chef_id))]
    already_booked = already_reviewed = False
    if "user_id" in session:
        uid = session["user_id"]
        already_booked   = bool(query(
            "SELECT 1 FROM booking WHERE user_id=? AND chef_id=?", (uid, chef_id), one=True))
        already_reviewed = bool(query(
            "SELECT 1 FROM review  WHERE user_id=? AND chef_id=?", (uid, chef_id), one=True))
    return render_template("chef_detail.html", chef=chef, reviews=reviews,
                           suggestions=suggestions,
                           already_booked=already_booked,
                           already_reviewed=already_reviewed)


@app.route("/book/<int:chef_id>", methods=["POST"])
@login_required
def book_chef(chef_id):
    chef = query("SELECT * FROM chef WHERE id=?", (chef_id,), one=True)
    if not chef:
        flash("Chef not found.", "danger")
        return redirect(url_for("chefs"))
    date      = request.form.get("date",      "").strip()
    time_slot = request.form.get("time_slot", "").strip()
    if not date or not time_slot:
        flash("Please select a date and time slot.", "danger")
        return redirect(url_for("chef_detail", chef_id=chef_id))
    execute("INSERT INTO booking (user_id,chef_id,date,time_slot) VALUES (?,?,?,?)",
            (session["user_id"], chef_id, date, time_slot))
    flash(f"Booking confirmed with {chef['name']} on {date} at {time_slot}!", "success")
    return redirect(url_for("dashboard"))


@app.route("/cancel_booking/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = query("SELECT * FROM booking WHERE id=?", (booking_id,), one=True)
    if not booking or booking["user_id"] != session["user_id"]:
        flash("Unauthorised action.", "danger")
        return redirect(url_for("dashboard"))
    execute("UPDATE booking SET status='Cancelled' WHERE id=?", (booking_id,))
    flash("Booking cancelled successfully.", "info")
    return redirect(url_for("dashboard"))


@app.route("/review/<int:chef_id>", methods=["POST"])
@login_required
def add_review(chef_id):
    rating  = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()
    if not rating or not (1 <= rating <= 5):
        flash("Please provide a valid rating (1–5).", "danger")
        return redirect(url_for("chef_detail", chef_id=chef_id))
    if query("SELECT 1 FROM review WHERE user_id=? AND chef_id=?",
             (session["user_id"], chef_id), one=True):
        flash("You have already reviewed this chef.", "warning")
        return redirect(url_for("chef_detail", chef_id=chef_id))
    execute("INSERT INTO review (user_id,chef_id,rating,comment) VALUES (?,?,?,?)",
            (session["user_id"], chef_id, rating, comment))
    flash("Your review has been submitted. Thank you!", "success")
    return redirect(url_for("chef_detail", chef_id=chef_id))


@app.route("/dashboard")
@login_required
def dashboard():
    uid  = session["user_id"]
    user = query("SELECT * FROM user WHERE id=?", (uid,), one=True)
    bookings = query("""
        SELECT b.*, c.name AS chef_name, c.cuisine, c.price, c.photo_url, c.id AS chef_id
        FROM booking b JOIN chef c ON c.id = b.chef_id
        WHERE b.user_id=? ORDER BY b.created_at DESC
    """, (uid,))
    reviews = query("""
        SELECT r.*, c.name AS chef_name, c.cuisine, c.photo_url
        FROM review r JOIN chef c ON c.id = r.chef_id
        WHERE r.user_id=? ORDER BY r.created_at DESC
    """, (uid,))
    return render_template("dashboard.html", user=user,
                           bookings=bookings, reviews=reviews)


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("✅  ChefCart running at http://localhost:5000")
    app.run(debug=True, port=5000)
