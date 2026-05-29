import 'dart:convert';
import 'package:http/http.dart' as http;

class TelegramService {
  static const String token = "7874069508:AAFTXxSlRM45b-5TsCEENtDkRxD7HuuAnj4";
  static const String botServer = "https://dental-bot-production-5bb4.up.railway.app";

  static Future<List<Map<String, dynamic>>> getAppointments() async {
    List<Map<String, dynamic>> appointments = [];
    try {
      final url = Uri.parse("$botServer/appointments");
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        for (var a in data) {
          appointments.add({
            'name': a['name'] ?? '',
            'time': a['time'] ?? '',
            'date': a['date'] ?? '',
          });
        }
      }
    } catch (e) {
      print('Xato: $e');
    }
    return appointments;
  }
}
