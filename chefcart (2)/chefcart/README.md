# 🍳 ChefCart – Smart Chef Booking Platform

A full-stack Flask web application to book professional chefs for home cooking.

---

## 📁 Project Structure

```
chefcart/
├── app.py                  ← Main Flask application (routes, models, logic)
├── requirements.txt        ← Python dependencies
├── instance/
│   └── chefcart.db         ← SQLite database (auto-created on first run)
├── templates/
│   ├── base.html           ← Layout with navbar & footer
│   ├── index.html          ← Homepage with top-rated chefs
│   ├── chefs.html          ← Browse & filter chefs
│   ├── chef_detail.html    ← Chef profile + booking + reviews
│   ├── dashboard.html      ← User booking history & reviews
│   ├── login.html          ← Login page
│   └── signup.html         ← Registration page
└── static/
    ├── css/
    │   └── style.css       ← All styles (warm editorial theme)
    └── js/
        └── main.js         ← Client-side interactions
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone or download the project
```bash
cd chefcart
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the application
```bash
python app.py
```

### Step 5 — Open in browser
```
http://localhost:5000
```

The database is created automatically on first run with 10 sample chefs and reviews.

---

## 🗄️ Database Schema

### `user` table
| Column   | Type    | Description               |
|----------|---------|---------------------------|
| id       | INTEGER | Primary key               |
| name     | TEXT    | Full name                 |
| email    | TEXT    | Unique email address      |
| password | TEXT    | Hashed password           |

### `chef` table
| Column     | Type    | Description                |
|------------|---------|----------------------------|
| id         | INTEGER | Primary key                |
| name       | TEXT    | Chef's name                |
| cuisine    | TEXT    | Cuisine specialization     |
| experience | INTEGER | Years of experience        |
| price      | REAL    | Price per session (₹)      |
| bio        | TEXT    | Short biography            |
| photo_url  | TEXT    | Profile photo URL          |

### `booking` table
| Column    | Type     | Description                   |
|-----------|----------|-------------------------------|
| id        | INTEGER  | Primary key                   |
| user_id   | INTEGER  | FK → user.id                  |
| chef_id   | INTEGER  | FK → chef.id                  |
| date      | TEXT     | Booking date (YYYY-MM-DD)     |
| time_slot | TEXT     | Time slot (e.g. "07:00 PM")   |
| status    | TEXT     | Confirmed / Cancelled         |
| created_at| DATETIME | Timestamp                     |

### `review` table
| Column    | Type     | Description                   |
|-----------|----------|-------------------------------|
| id        | INTEGER  | Primary key                   |
| user_id   | INTEGER  | FK → user.id                  |
| chef_id   | INTEGER  | FK → chef.id                  |
| rating    | INTEGER  | 1–5 stars                     |
| comment   | TEXT     | Optional comment              |
| created_at| DATETIME | Timestamp                     |

---

## 🎯 Features Summary

| Feature                   | Details                                              |
|---------------------------|------------------------------------------------------|
| Authentication            | Signup, Login, Logout with hashed passwords          |
| Chef Listing              | 10 sample chefs with photos, ratings, and bios       |
| Search & Filter           | By cuisine, price range, minimum rating              |
| Booking System            | Date + time-slot picker, booking confirmation        |
| Cancel Booking            | Users can cancel their own bookings                  |
| Reviews & Ratings         | 1–5 star picker + comments, average auto-calculated  |
| Recommendation System     | Top-rated chefs on homepage; similar chefs on detail |
| Dashboard                 | Full booking history + review history                |
| Responsive Design         | Works on desktop, tablet, and mobile                 |

---

## 🔑 Test Credentials

Register any account via `/signup` — there are no pre-seeded user accounts.

Sample chefs (auto-seeded):
- Arjun Mehta — North Indian — ₹2,500
- Priya Nair — South Indian — ₹2,000
- Rahul Sharma — Chinese — ₹2,200
- Sunita Reddy — Continental — ₹3,500
- Vikram Patel — Mughlai — ₹2,800
- ...and 5 more!
