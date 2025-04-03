import os
import cv2
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Retrieve environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate environment variables
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing Gemini API Key in .env file.")

# Ensure frames output folder exists
os.makedirs("frames_output", exist_ok=True)

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to send image to Gemini API
def analyze_frame(image_path):
    base64_image = encode_image(image_path)
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        json={
            "contents": [
                {
                    "parts": [
                        {"text": "Analyze this image and determine if a person is falling, lying on the ground unnaturally, or appears unconscious. If none, respond with 'No Fall Detected'."},
                        {"inlineData": {"mimeType": "image/jpeg", "data": base64_image}}
                    ]
                }
            ]
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "no response").lower()
    return "no response"

# API Endpoint to process video
@app.route("/detect_fall", methods=["POST"])
def detect_fall():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    video_path = "fall_detection_video.mp4"
    file.save(video_path)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fall_detected = False
    fall_count = 0  # Count fall detections
    fall_threshold = 3  # Minimum frames required for confirmation
    detected_fall_frame = None  # Store fall detected frame path

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = f"frames_output/frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)

        prediction = analyze_frame(frame_filename)
        print(f"{frame_filename}: {prediction}")

        if "no person" in prediction or "no fall detected" in prediction:
            continue

        if "falling position" in prediction or "lying on the ground" in prediction or "unconscious" in prediction:
            fall_count += 1
            detected_fall_frame = frame_filename  # Store the first detected fall frame
        else:
            fall_count = 0  # Reset count if no fall is detected

        if fall_count >= fall_threshold:
            fall_detected = True
            break  # Stop processing once a fall is confirmed

        frame_count += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    cap.release()

    if fall_detected and detected_fall_frame:
        encoded_frame = encode_image(detected_fall_frame)
        return jsonify({
            "status": "Fall Detected",
            "alert": "🚨 Fall detected in video!",
            "fall_frame": encoded_frame  # Sending the detected frame as base64
        })
    
    return jsonify({"status": "No Fall Detected", "message": "No fall detected in the video."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
