import cv2
import os

from flask import Flask, render_template, request, redirect, send_file, session
from engine.feature_extractor import extract_url_features
from engine.rule_engine import calculate_rule_risk
from engine.ml_detector import predict_ml_probability
from engine.risk_calculator import calculate_final_risk
from engine.explanation_engine import generate_explanation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from database import db

app = Flask(__name__)

# CONFIG FIRST
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phishguard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# THEN INIT
db.init_app(app)

# IMPORTING MODELS AFTER INIT
from models.db_models import User, Post

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/qr-scan")
def qr_scan():
    return render_template("qr_scan.html")

@app.route("/awareness")
def awareness():
    return render_template("awareness.html")

@app.route("/community")
def community():
    if "user_id" not in session:
        return redirect("/login_page")
    return render_template("community.html")

@app.route("/login_page")
def login_page():
    if "user_id" in session:
        return redirect("/community")
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Basic validation
    if not username or not email or not password:
        return "All fields are required"

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "User already exists"

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    return redirect("/login_page")

app.secret_key = "secret123" 

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return "Missing credentials"

    user = User.query.filter_by(email=email).first()

    if not user:
        return "User not found"

    if user.password != password:
        return "Incorrect password"

    # Login success
    session["user_id"] = user.id
    session["username"] = user.username

    return redirect("/community")
    


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/create_post", methods=["POST"])
def create_post():

    if "user_id" not in session:
        return redirect("/login_page")

    content = request.form.get("content")

    if not content:
        return redirect("/community")

    post = Post(
        content=content,
        user_id=session["user_id"]
    )

    db.session.add(post)
    db.session.commit()

    return redirect("/community")

@app.route("/analyze_qr", methods=["POST"])
def analyze_qr():

    file = request.files["qr_image"]

    if not file:
        return redirect("/")

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Read image using OpenCV
    img = cv2.imread(filepath)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if not data:
        return render_template("result.html",
                               error="No QR code detected.")

    qr_url = data

    features = extract_url_features(qr_url)
    ml_prob = predict_ml_probability(features)
    rule_score = calculate_rule_risk(features)
    result = calculate_final_risk(ml_prob, rule_score, features)
    explanation = generate_explanation(
    features,
    rule_score,
    result["final_risk"],
    result["classification"]
)

    return render_template("result.html",
                           url=qr_url,
                           result=result,
                           explanation=explanation)



@app.route("/analyze", methods=["POST"])
def analyze():

    url = request.form.get("url")

    if not url:
        return render_template("result.html",
                               error="Please enter a valid URL.")

    # Step 1: Extract features
    features = extract_url_features(url)

    # Step 2: ML probability
    ml_prob = predict_ml_probability(features)

    # Step 3: Rule score
    rule_score = calculate_rule_risk(features)

    # Step 4: Final risk
    result = calculate_final_risk(
        ml_probability=ml_prob,
        rule_score=rule_score,
        features=features
    )

    # Step 5: Explanation
    explanation = generate_explanation(
        features,
        rule_score,
        result["final_risk"],
        result["classification"]
    )

    return render_template("result.html",
                           url=url,
                           result=result,
                           explanation=explanation)

@app.route("/download_report")
def download_report():

    filepath = "reports/report.pdf"
    c = canvas.Canvas(filepath, pagesize=letter)

    c.drawString(50, 750, "Phishing Detection Report")
    c.drawString(50, 730, f"URL: {request.args.get('url')}")
    c.drawString(50, 710, f"Risk: {request.args.get('risk')}%")
    c.drawString(50, 690, f"Classification: {request.args.get('class')}")

    c.save()

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
