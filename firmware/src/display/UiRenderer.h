#pragma once
#include <Arduino.h>
#include "../protocol/UsageState.h"

class UiRenderer {
public:
  void begin();
  void render(const UsageState& state);
private:
  uint32_t lastRenderMs = 0;
};
