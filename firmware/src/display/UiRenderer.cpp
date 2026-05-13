#include "UiRenderer.h"

void UiRenderer::begin() {
  // TODO: initialize board-specific display driver here.
  // Start from your Waveshare example, then replace Serial output with drawing.
  Serial.println("UiRenderer ready");
}

void UiRenderer::render(const UsageState& state) {
  uint32_t now = millis();
  if (now - lastRenderMs < 1000) return;
  lastRenderMs = now;

  // Placeholder renderer for serial monitor until display driver is wired.
  Serial.print("[meter] ");
  Serial.print(state.currentPercent);
  Serial.print("% current / ");
  Serial.print(state.weeklyPercent);
  Serial.print("% weekly / ");
  Serial.print(state.burnRate);
  Serial.print(" / ");
  Serial.print(state.status);
  Serial.print(" / confidence=");
  Serial.println(state.confidence);
}
