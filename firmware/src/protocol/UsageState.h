#pragma once
#include <Arduino.h>

struct UsageState {
  String schema = "ai-desk-meter.v1";
  String service = "mock";
  float currentPercent = 0;
  float weeklyPercent = 0;
  uint32_t currentResetSeconds = 0;
  uint32_t weeklyResetSeconds = 0;
  String burnRate = "idle";
  String status = "Boot";
  String mode = "boot";
  uint32_t updatedAt = 0;
  String source = "firmware";
  String confidence = "unknown";
};
