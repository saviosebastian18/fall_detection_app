# // import 'package:flutter/material.dart';
# // import 'package:http/http.dart' as http;
# // import 'dart:convert';
# // import 'dart:io';
# // import 'package:file_picker/file_picker.dart';

# // void main() {
# //   runApp(const MyApp());
# // }

# // class MyApp extends StatelessWidget {
# //   const MyApp({super.key});

# //   @override
# //   Widget build(BuildContext context) {
# //     return MaterialApp(
# //       title: 'Fall Detection App',
# //       debugShowCheckedModeBanner: false,
# //       routes: {
# //         '/': (context) => const HomePage(),
# //         '/add': (context) => const AddUser(),
# //         '/upload': (context) => const UploadVideo(),
# //       },
# //       initialRoute: '/',
# //     );
# //   }
# // }

# // class HomePage extends StatelessWidget {
# //   const HomePage({super.key});

# //   @override
# //   Widget build(BuildContext context) {
# //     return Scaffold(
# //       appBar: AppBar(
# //         title: const Text("Fall Detection App"),
# //         backgroundColor: Colors.red,
# //       ),
# //       body: Center(
# //         child: ElevatedButton(
# //           onPressed: () {
# //             Navigator.pushNamed(context, '/upload');
# //           },
# //           child: const Text('Upload Video for Fall Detection'),
# //         ),
# //       ),
# //       floatingActionButton: FloatingActionButton(
# //         onPressed: () {
# //           Navigator.pushNamed(context, '/add');
# //         },
# //         backgroundColor: Colors.red,
# //         child: const Icon(Icons.add, size: 40),
# //       ),
# //       floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
# //     );
# //   }
# // }

# // class UploadVideo extends StatefulWidget {
# //   const UploadVideo({super.key});

# //   @override
# //   State<UploadVideo> createState() => _UploadVideoState();
# // }

# // class _UploadVideoState extends State<UploadVideo> {
# //   File? _video;
# //   String _result = '';
# //   final String flaskUrl = 'http://172.16.14.82:5000/detect_fall'; // Replace with your Flask backend URL

# //   Future<void> _pickVideo() async {
# //     final result = await FilePicker.platform.pickFiles(type: FileType.video);
# //     if (result != null && result.files.single.path != null) {
# //       setState(() {
# //         _video = File(result.files.single.path!);
# //       });
# //     }
# //   }

# //   Future<void> _uploadVideo() async {
# //     if (_video == null) {
# //       ScaffoldMessenger.of(context).showSnackBar(
# //         const SnackBar(content: Text('Please select a video first.')),
# //       );
# //       return;
# //     }

# //     try {
# //       var request = http.MultipartRequest('POST', Uri.parse(flaskUrl));
# //       request.files.add(await http.MultipartFile.fromPath('video', _video!.path));

# //       var response = await request.send();
# //       var responseData = await response.stream.bytesToString();

# //       if (response.statusCode == 200) {
# //         var jsonData = jsonDecode(responseData);
# //         setState(() {
# //           _result = jsonData['status'] ?? 'Unknown response';
# //         });
# //       } else {
# //         setState(() {
# //           _result = 'Error uploading video: ${response.reasonPhrase}';
# //         });
# //       }
# //     } catch (e) {
# //       setState(() {
# //         _result = 'Error: $e';
# //       });
# //     }
# //   }

# //   @override
# //   Widget build(BuildContext context) {
# //     return Scaffold(
# //       appBar: AppBar(
# //         title: const Text("Upload Video"),
# //         backgroundColor: Colors.red,
# //       ),
# //       body: Padding(
# //         padding: const EdgeInsets.all(15.0),
# //         child: Column(
# //           mainAxisAlignment: MainAxisAlignment.center,
# //           children: [
# //             ElevatedButton(
# //               onPressed: _pickVideo,
# //               child: const Text('Pick Video'),
# //             ),
# //             const SizedBox(height: 10),
# //             _video != null
# //                 ? Text('Video selected: ${_video!.path}')
# //                 : const Text('No video selected'),
# //             const SizedBox(height: 20),
# //             ElevatedButton(
# //               onPressed: _uploadVideo,
# //               child: const Text('Upload and Analyze'),
# //             ),
# //             const SizedBox(height: 20),
# //             Text(
# //               _result,
# //               style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
# //             ),
# //           ],
# //         ),
# //       ),
# //     );
# //   }
# // }

# // class AddUser extends StatefulWidget {
# //   const AddUser({super.key});

# //   @override
# //   State<AddUser> createState() => _AddUserState();
# // }

# // class _AddUserState extends State<AddUser> {
# //   final _formKey = GlobalKey<FormState>();
# //   final TextEditingController _nameController = TextEditingController();
# //   final TextEditingController _phoneController = TextEditingController();
# //   final TextEditingController _passwordController = TextEditingController();
# //   final String flaskUrl = 'http://172.16.14.82:5000/add_user'; // Replace with your backend URL

# //   Future<void> _submitForm() async {
# //     if (_formKey.currentState!.validate()) {
# //       final response = await http.post(
# //         Uri.parse(flaskUrl),
# //         headers: {'Content-Type': 'application/json'},
# //         body: jsonEncode({
# //           'name': _nameController.text,
# //           'phone': _phoneController.text,
# //           'password': _passwordController.text,
# //         }),
# //       );

# //       if (response.statusCode == 200) {
# //         ScaffoldMessenger.of(context).showSnackBar(
# //           const SnackBar(content: Text('User added successfully!')),
# //         );
# //         Navigator.pop(context);
# //       } else {
# //         ScaffoldMessenger.of(context).showSnackBar(
# //           const SnackBar(content: Text('Error adding user.')),
# //         );
# //       }
# //     }
# //   }

# //   @override
# //   Widget build(BuildContext context) {
# //     return Scaffold(
# //       appBar: AppBar(
# //         title: const Text("Add Users"),
# //         backgroundColor: Colors.red,
# //       ),
# //       body: Padding(
# //         padding: const EdgeInsets.all(15.0),
# //         child: Form(
# //           key: _formKey,
# //           child: Column(
# //             children: [
# //               Padding(
# //                 padding: const EdgeInsets.all(8.0),
# //                 child: TextFormField(
# //                   controller: _nameController,
# //                   decoration: const InputDecoration(
# //                     border: OutlineInputBorder(),
# //                     labelText: 'User Name',
# //                   ),
# //                   validator: (value) {
# //                     if (value == null || value.isEmpty) {
# //                       return 'Please enter a name';
# //                     }
# //                     return null;
# //                   },
# //                 ),
# //               ),
# //               Padding(
# //                 padding: const EdgeInsets.all(8.0),
# //                 child: TextFormField(
# //                   controller: _phoneController,
# //                   keyboardType: TextInputType.number,
# //                   maxLength: 10,
# //                   decoration: const InputDecoration(
# //                     border: OutlineInputBorder(),
# //                     labelText: 'Phone Number',
# //                   ),
# //                   validator: (value) {
# //                     if (value == null || value.length != 10) {
# //                       return 'Enter a valid 10-digit phone number';
# //                     }
# //                     return null;
# //                   },
# //                 ),
# //               ),
# //               ElevatedButton(
# //                 onPressed: _submitForm,
# //                 child: const Text("Submit"),
# //               ),
# //             ],
# //           ),
# //         ),
# //       ),
# //     );
# //   }
# // }
# # 








# import os
# import cv2
# import base64
# import requests
# import jwt
# from jwt.algorithms import RSAAlgorithm
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# from supabase import create_client, Client

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# # Retrieve environment variables
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Validate environment variables
# if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_SECRET_KEY, GEMINI_API_KEY]):
#     raise ValueError("❌ Missing Supabase URL, Key, Service Key, or Gemini API Key in .env file.")

# # Create Supabase client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Ensure frames output folder exists
# os.makedirs("frames_output", exist_ok=True)

# # Function to fetch Supabase public keys (JWKS) for RS256 verification
# def get_supabase_jwks():
#     """Fetch Supabase public JWKS for RS256 verification."""
#     try:
#         url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         print("❌ Failed to fetch Supabase JWKS.")
#         return None
#     except Exception as e:
#         print("❌ Error fetching JWKS:", e)
#         return None

# # Function to verify Supabase JWT token
# def verify_user(token):
#     try:
#         if not token:
#             print("❌ No token received.")
#             return False

#         # Decode token WITHOUT verification first (to check algorithm)
#         header = jwt.get_unverified_header(token)
#         print("🔍 JWT Header:", header)

#         alg = header.get("alg")
#         if alg == "HS256":  # Service Role Token
#             decoded_token = jwt.decode(
#                 token,
#                 SUPABASE_SECRET_KEY,
#                 algorithms=["HS256"],
#                 options={"verify_aud": False}
#             )
#         elif alg == "RS256":  # User Token
#             jwks = get_supabase_jwks()
#             if not jwks:
#                 print("❌ Failed to fetch Supabase public keys.")
#                 return False

#             key_id = header.get("kid")
#             public_keys = {key["kid"]: key for key in jwks["keys"]}
#             if key_id not in public_keys:
#                 print("❌ No matching key ID found in JWKS.")
#                 return False

#             # Convert JWKS to public key
#             public_key = RSAAlgorithm.from_jwk(public_keys[key_id])
#             print(f"🟢 Using Public Key: {public_key}")

#             decoded_token = jwt.decode(
#                 token,
#                 public_key,
#                 algorithms=["RS256"],
#                 options={"verify_aud": False}
#             )
#         else:
#             print(f"❌ Unsupported algorithm: {alg}")
#             return False

#         print("✅ Token Verified Successfully:", decoded_token)
#         return decoded_token.get("sub") is not None
#     except jwt.ExpiredSignatureError:
#         print("❌ Token expired.")
#         return False
#     except jwt.InvalidTokenError:
#         print("❌ Invalid token.")
#         return False

# # Function to encode image to base64
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# # Function to send image to Gemini API
# def analyze_frame(image_path):
#     base64_image = encode_image(image_path)
#     response = requests.post(
#         f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
#         json={
#             "contents": [
#                 {
#                     "parts": [
#                         {"text": "Analyze this image and determine if a person is falling, lying on the ground unnaturally, or appears unconscious. If none, respond with 'No Fall Detected'."},
#                         {"inlineData": {"mimeType": "image/jpeg", "data": base64_image}}
#                     ]
#                 }
#             ]
#         }
#     )
    
#     if response.status_code == 200:
#         result = response.json()
#         return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "no response").lower()
#     return "no response"

# # API Endpoint to process video
# @app.route("/detect_fall", methods=["POST"])
# def detect_fall():
#     token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
#     if not token or not verify_user(token):
#         return jsonify({"error": "Unauthorized"}), 401

#     if "video" not in request.files:
#         return jsonify({"error": "No video file provided"}), 400

#     file = request.files["video"]
#     video_path = "fall_detection_video.mp4"
#     file.save(video_path)

#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     fall_detected = False
#     fall_count = 0  # Count fall detections
#     fall_threshold = 3  # Minimum frames required for confirmation

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_filename = f"frames_output/frame_{frame_count}.jpg"
#         cv2.imwrite(frame_filename, frame)

#         prediction = analyze_frame(frame_filename)
#         print(f"{frame_filename}: {prediction}")

#         if "no person" in prediction or "no fall detected" in prediction:
#             continue

#         if "falling position" in prediction or "lying on the ground" in prediction or "unconscious" in prediction:
#             fall_count += 1
#         else:
#             fall_count = 0  # Reset count if no fall is detected

#         if fall_count >= fall_threshold:
#             fall_detected = True
#             break  # Stop processing once a fall is confirmed

#         frame_count += 5
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

#     cap.release()

#     if fall_detected:
#         return jsonify({"status": "Fall Detected", "alert": "🚨 Fall detected in video!"})
#     return jsonify({"status": "No Fall Detected", "message": "No fall detected in the video."})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)




























import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:fall_detection_app/home_page.dart';
import 'package:fall_detection_app/login_screen.dart';
import 'package:fall_detection_app/signup_screen.dart';
import 'dart:typed_data';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Supabase.initialize(
    url: 'https://kzlkbjcsszpemqrvzvfc.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6bGtiamNzc3pwZW1xcnZ6dmZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI2NjI3NzMsImV4cCI6MjA1ODIzODc3M30.fnQlMUo2B8LTkmv3Qds9bDWu00afsYSIkZolJeUKcVI',
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fall Detection App',
      debugShowCheckedModeBanner: false,
      routes: {
        '/': (context) => const HomePage(),
        '/login': (context) => LoginScreen(),
        '/signup': (context) => SignUpScreen(),
        '/upload': (context) => const UploadVideoScreen(),
      },
      initialRoute: '/login',
    );
  }
}

/// Screen for Uploading a Video for Fall Detection
class UploadVideoScreen extends StatefulWidget {
  const UploadVideoScreen({super.key});

  @override
  State<UploadVideoScreen> createState() => _UploadVideoScreenState();
}

class _UploadVideoScreenState extends State<UploadVideoScreen> {
  File? _video;
  String _result = '';
  Uint8List? _fallImage; // Stores the detected fall frame image
  final supabase = Supabase.instance.client;
  final String flaskServerUrl = "http://127.0.0.1:5000"; // Change for hosted server

  /// Picks a video from the user's device
  Future<void> _pickVideo() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.video);
    if (result != null && result.files.single.path != null) {
      setState(() {
        _video = File(result.files.single.path!);
        _fallImage = null; // Reset fall image when selecting a new video
        _result = "Video selected: ${_video!.path}";
      });
    }
  }

  /// Uploads the selected video to the Flask backend
  Future<void> _uploadVideo() async {
    final user = supabase.auth.currentUser;
    if (user == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please log in first.')),
      );
      Navigator.pushNamed(context, '/login');
      return;
    }

    // 🔹 Refresh session to get a valid token
    await supabase.auth.refreshSession();
    final session = supabase.auth.currentSession;
    final accessToken = session?.accessToken ?? '';

    print("🟢 Supabase Access Token: $accessToken"); // Debugging

    if (accessToken.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Authentication failed. Please log in again.')),
      );
      return;
    }

    if (_video == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a video.')),
      );
      return;
    }

    try {
      var request = http.MultipartRequest('POST', Uri.parse('$flaskServerUrl/detect_fall'));
      request.headers['Authorization'] = 'Bearer $accessToken';
      request.files.add(await http.MultipartFile.fromPath('video', _video!.path));

      var response = await request.send();
      var responseData = await response.stream.bytesToString();

      print("🔵 Response Status Code: ${response.statusCode}");
      print("🔵 Response Data: $responseData");

      if (response.statusCode == 200) {
        var jsonData = jsonDecode(responseData);
        setState(() {
          _result = jsonData['status'] ?? 'Unknown response';
          if (jsonData.containsKey("fall_frame")) {
            _fallImage = base64Decode(jsonData["fall_frame"]);
          }
        });
      } else {
        var errorResponse = jsonDecode(responseData);
        setState(() {
          _result = 'Error: ${errorResponse['error'] ?? response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Upload Video"),
        backgroundColor: Colors.red,
      ),
      body: Padding(
        padding: const EdgeInsets.all(15.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickVideo,
              child: const Text('Pick Video'),
            ),
            const SizedBox(height: 10),
            _video != null
                ? Text('Video selected: ${_video!.path}')
                : const Text('No video selected'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _uploadVideo,
              child: const Text('Upload and Analyze'),
            ),
            const SizedBox(height: 20),
            Text(
              _result,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            _fallImage != null
                ? Column(
                    children: [
                      const Text(
                        "Detected Fall Frame:",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 10),
                      Image.memory(_fallImage!, width: 300, height: 200),
                    ],
                  )
                : const SizedBox(),
          ],
        ),
      ),
    );
  }
}
