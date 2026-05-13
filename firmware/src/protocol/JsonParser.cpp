#include "JsonParser.h"
#include <ArduinoJson.h>

static float clampPercent(float value) {
  if (value < 0) return 0;
  if (value > 100) return 100;
  return value;
}

ParseResult parseUsageJson(const String& body, UsageState& state) {
  JsonDocument doc;
  DeserializationError err = deserializeJson(doc, body);
  if (err) return {false, err.c_str()};

  const char* schema = doc["schema"] | "";
  if (String(schema) != "ai-desk-meter.v1") {
    return {false, "schema mismatch"};
  }

  state.schema = schema;
  state.service = (const char*)(doc["service"] | "unknown");
  state.currentPercent = clampPercent(doc["current_percent"] | 0.0);
  state.weeklyPercent = clampPercent(doc["weekly_percent"] | 0.0);
  state.currentResetSeconds = doc["current_reset_seconds"] | 0;
  state.weeklyResetSeconds = doc["weekly_reset_seconds"] | 0;
  state.burnRate = (const char*)(doc["burn_rate"] | "normal");
  state.status = (const char*)(doc["status"] | "Ready");
  state.mode = (const char*)(doc["mode"] | "active");
  state.updatedAt = doc["updated_at"] | 0;
  state.source = (const char*)(doc["source"] | "unknown");
  state.confidence = (const char*)(doc["confidence"] | "unknown");
  return {true, ""};
}
