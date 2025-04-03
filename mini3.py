import cv2
import requests
import base64
import os

#  YOUR GEMINI API KEY (Hardcoded)
API_KEY = "AIzaSyBCa6-B8L0isD81EpBzkHqVa674SCQD8vk"

#  Create a folder to save frames
if not os.path.exists('frames_output'):
    os.makedirs('frames_output')

#  Function to convert image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#  Function to send image to Gemini API
def analyze_frame(image_path):
    base64_image = encode_image(image_path)
    
    # Fixed Gemini 1.5 API URL
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}",
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Analyze this image and tell me if the person has fallen or not."
                        },
                        {
                            "inlineData": {
                                "mimeType": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }
    )
    
    #  Check response
    if response.status_code == 200:
        result = response.json()
        output_text = result['candidates'][0]['content']['parts'][0]['text']
        return output_text
    else:
        return "NO RESPONSE"

#  Function to capture frames from the video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fall_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #  Save frame as image
        frame_filename = f'frames_output/frame_{frame_count}.jpg'
        cv2.imwrite(frame_filename, frame)

        #  Send frame to Gemini API
        prediction = analyze_frame(frame_filename)
        print(f"{frame_filename}: {prediction}")

        #  Check if fall is detected
        if "fall" in prediction.lower() or "person fell" in prediction.lower():
            fall_detected = True
            cv2.putText(frame, "🚨 FALL DETECTED 🚨", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("🚨 ALERT: FALL DETECTED IN VIDEO 🚨")
        
        #  Display the video
        cv2.imshow("Fall Detection System", frame)
        frame_count += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

        #  Break the loop when the video ends or key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#  Run the video processing
video_path = "fal_detection_video.mp4"  # Provide your recorded video here
process_video(video_path)
