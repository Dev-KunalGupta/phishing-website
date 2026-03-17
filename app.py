import cv2
import numpy as np

from PIL import Image
import os

from flask import Flask, render_template, request
from engine.feature_extractor import extract_url_features
from engine.rule_engine import calculate_rule_risk
from engine.ml_detector import predict_ml_probability
from engine.risk_calculator import calculate_final_risk
from engine.explanation_engine import generate_explanation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report")
def report():
    return render_template("report.html")

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
    rule_score = calculate_rule_score(features)
    result = calculate_final_risk(ml_prob, rule_score, features)
    explanation = generate_explanation(features)

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
