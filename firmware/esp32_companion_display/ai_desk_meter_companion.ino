#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "your-wifi";
const char* WIFI_PASS = "your-password";
const char* STATUS_URL = "http://192.168.1.50:8787/companion/status?provider=mock";
const unsigned long POLL_MS = 5000;

struct CompanionState {
  int currentPct = 0;
  int weeklyPct = 0;
  String currentReset = "0m";
  String weeklyReset = "0m";
  String activity = "musing";
  String message = "✶ Musing...";
  String status = "offline";
  int warnings = 0;
  int errors = 0;
};

CompanionState state;
unsigned long lastPoll = 0;

// 10x5 exact public pixel-buddy silhouette reference: O=orange, B=blue, .=empty.
const char* PIXEL_BUDDY[5] = {
  "..OOOOOO..",
  ".OOOOOOOO.",
  "OOOOOOOOOO",
  "..OOOOOO..",
  ".BB....BB."
};

void renderSerial() {
  Serial.println("--- AI Desk Meter Companion ---");
  Serial.printf("Current: %d%% reset %s\n", state.currentPct, state.currentReset.c_str());
  Serial.printf("Weekly : %d%% reset %s\n", state.weeklyPct, state.weeklyReset.c_str());
  Serial.printf("State  : %s / %s\n", state.status.c_str(), state.activity.c_str());
  for (int row = 0; row < 5; row++) Serial.println(PIXEL_BUDDY[row]);
  Serial.println(state.message);
  Serial.printf("Warnings: %d Errors: %d\n", state.warnings, state.errors);
}

bool applyPayload(const String& body) {
  StaticJsonDocument<768> doc;
  DeserializationError err = deserializeJson(doc, body);
  if (err) {
    state.status = "error";
    state.activity = "error";
    state.message = "Bad JSON";
    return false;
  }
  const char* schema = doc["schema"] | "";
  if (String(schema) != "ai_desk_meter_companion_v1") {
    state.status = "error";
    state.activity = "error";
    state.message = "Schema mismatch";
    return false;
  }
  state.currentPct = constrain((int)(doc["current_pct"] | 0), 0, 100);
  state.weeklyPct = constrain((int)(doc["weekly_pct"] | 0), 0, 100);
  state.currentReset = (const char*)(doc["current_reset"] | "0m");
  state.weeklyReset = (const char*)(doc["weekly_reset"] | "0m");
  state.activity = (const char*)(doc["activity"] | "musing");
  state.message = (const char*)(doc["message"] | "✶ Musing...");
  state.status = (const char*)(doc["status"] | "linked");
  state.warnings = doc["warnings"] | 0;
  state.errors = doc["errors"] | 0;
  return true;
}

void pollStatus() {
  if (WiFi.status() != WL_CONNECTED) {
    state.status = "offline";
    state.activity = "offline";
    state.message = "Wi-Fi offline";
    return;
  }
  HTTPClient http;
  http.begin(STATUS_URL);
  int code = http.GET();
  if (code == 200) {
    applyPayload(http.getString());
  } else {
    state.status = "error";
    state.activity = "error";
    state.message = "HTTP " + String(code);
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(300);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long now = millis();
  if (now - lastPoll >= POLL_MS) {
    lastPoll = now;
    pollStatus();
    renderSerial();
  }
}
