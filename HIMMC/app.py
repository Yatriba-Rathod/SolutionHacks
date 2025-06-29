from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import bcrypt
from db import users_collection, jobs_collection
from gemini_api import generate_job_postings, generate_task, generate_feedback

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
CORS(app)


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users_collection.find_one({
            "email": {"$regex": f"^{email}$", "$options": "i"}
        })

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            session["user_id"] = str(user["_id"])
            session["email"] = user["email"]
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if users_collection.find_one({"email": email}):
            flash("Email already registered. Please log in.", "error")
            return redirect("/signup")

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        users_collection.insert_one({"email": email, "password": hashed_pw, "xp": 0})
        session["email"] = email
        return redirect("/simulator")

    return render_template("signup.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user = users_collection.find_one({"_id": ObjectId(session["user_id"])})
    xp = user.get("xp", 0)
    return render_template("dashboard.html", email=user["email"], xp=xp)


@app.route("/simulator")
def simulator():
    if "user_id" not in session:
        return redirect("/login")
    company = request.args.get("company")
    role = request.args.get("role")
    return render_template("simulator.html", company=company, role=role)


@app.route("/api/task")
def get_task():
    company = request.args.get("company")
    role = request.args.get("role")
    if not company or not role:
        return jsonify({"error": "Missing company or role"}), 400

    task_text = generate_task(role, company)
    return jsonify({"task": task_text})


@app.route("/api/feedback", methods=["POST"])
def generate_feedback_route():
    task_response = request.form.get("text")
    role = request.form.get("role")
    if not task_response or not role:
        return jsonify({"error": "Missing task response or role"}), 400

    feedback, xp = generate_feedback(task_response, role)

    if "user_id" in session:
        users_collection.update_one(
            {"_id": ObjectId(session["user_id"])},
            {"$inc": {"xp": xp}}
        )

    return jsonify({"feedback": feedback, "xp_awarded": xp})


@app.route("/job_finder", methods=["GET", "POST"])
def job_finder():
    if request.method == "POST":
        role = request.form.get("role")
        location = request.form.get("location")
        filters = {
            "adhd": "adhd" in request.form,
            "disability": "disability" in request.form,
            "no_degree": "no_degree" in request.form,
        }
        pay_range = request.form.get("pay_range")

        jobs = generate_job_postings(role, location, filters, pay_range)

        # Filter out duplicates
        inserted_jobs = []
        for job in jobs:
            existing = jobs_collection.find_one({"apply_url": job["apply_url"]})
            if not existing:
                jobs_collection.insert_one(job)
                inserted_jobs.append(job)

        # Include existing jobs matching role+location
        db_jobs = list(jobs_collection.find({
            "role": {"$regex": role, "$options": "i"},
            "location": {"$regex": location, "$options": "i"}
        }))

        return render_template("job_finder.html", jobs=db_jobs + inserted_jobs)

    return render_template("job_finder.html", jobs=[])


if __name__ == "__main__":
    app.run(debug=True)
