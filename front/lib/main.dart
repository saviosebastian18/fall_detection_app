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