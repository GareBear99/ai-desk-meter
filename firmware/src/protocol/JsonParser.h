#pragma once
#include <Arduino.h>
#include "UsageState.h"

struct ParseResult {
  bool ok;
  String error;
};

ParseResult parseUsageJson(const String& body, UsageState& state);
