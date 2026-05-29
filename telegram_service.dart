import 'dart:convert';
import 'package:http/http.dart' as http;

class TelegramService {
  static const String token = "7874069508:AAFTXxSlRM45b-5TsCEENtDkRxD7HuuAnj4";

  static Future<List<Map<String, dynamic>>> getAppointments() async {
    List<Map<String, dynamic>> appointments = [];
    try {
      final url = Uri.parse("https://api.telegram.org/bot$token/getUpdates");
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        for (var update in data['result']) {
          if (update['message'] != null) {
            String text = update['message']['text'] ?? '';
            Map<String, String> parsed = {};
            List<String> lines = text.split('\n');
            for (var line in lines) {
              if (line.contains(':')) {
                List<String> parts = line.split(':');
                String key = parts[0].trim().toLowerCase();
                String value = parts[1].trim();
                parsed[key] = value;
              }
            }
            if (parsed.containsKey('ism') && parsed.containsKey('soat')) {
              appointments.add({
                'name': parsed['ism'] ?? '',
                'time': parsed['soat'] ?? '',
                'date': parsed['sana'] ?? '',
              });
            }
          }
        }
      }
    } catch (e) {
      print('Xato: $e');
    }
    return appointments;
  }
}
