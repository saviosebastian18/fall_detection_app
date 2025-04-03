import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class UploadVideoScreen extends StatefulWidget {
  const UploadVideoScreen({super.key});

  @override
  State<UploadVideoScreen> createState() => _UploadVideoScreenState();
}

class _UploadVideoScreenState extends State<UploadVideoScreen> {
  File? _video;
  String _result = '';
  final supabase = Supabase.instance.client;
  final String flaskServerUrl = "http://127.0.0.1:5000"; // Change if using a hosted server

  /// Picks a video file from the device
  Future<void> _pickVideo() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.video);
    if (result != null && result.files.single.path != null) {
      setState(() {
        _video = File(result.files.single.path!);
      });
    }
  }

  /// Uploads the video to the Flask backend for fall detection
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

      if (response.statusCode == 200) {
        var jsonData = jsonDecode(responseData);
        setState(() {
          _result = jsonData['status'] ?? 'Unknown response';
        });
      } else {
        setState(() {
          _result = 'Error uploading video: ${jsonDecode(responseData)['error'] ?? response.reasonPhrase}';
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
            _video != null ? Text('Video selected: ${_video!.path}') : const Text('No video selected'),
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
          ],
        ),
      ),
    );
  }
}
