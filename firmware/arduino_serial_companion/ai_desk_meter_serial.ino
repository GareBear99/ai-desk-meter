#include <ArduinoJson.h>

String line;

void renderState(JsonDocument& doc) {
  Serial.println("--- AI Desk Meter Serial Companion ---");
  Serial.print("Current: "); Serial.print((int)(doc["current_pct"] | 0)); Serial.println("%");
  Serial.print("Weekly : "); Serial.print((int)(doc["weekly_pct"] | 0)); Serial.println("%");
  Serial.print("State  : "); Serial.println((const char*)(doc["activity"] | "musing"));
  Serial.println((const char*)(doc["message"] | "✶ Musing..."));
}

void setup() {
  Serial.begin(115200);
  Serial.println("AI Desk Meter Arduino serial companion ready");
}

void loop() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      StaticJsonDocument<512> doc;
      DeserializationError err = deserializeJson(doc, line);
      if (err) {
        Serial.println("Bad JSON");
      } else if (String((const char*)(doc["schema"] | "")) != "ai_desk_meter_companion_v1") {
        Serial.println("Schema mismatch");
      } else {
        renderState(doc);
      }
      line = "";
    } else if (line.length() < 480) {
      line += c;
    }
  }
}
