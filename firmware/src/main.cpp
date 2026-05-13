#include <Arduino.h>
#include "protocol/UsageState.h"
#include "protocol/JsonParser.h"
#include "display/UiRenderer.h"
#include "transport/WifiServer.h"

UsageState state;
UiRenderer ui;
WifiServerTransport wifi;

void onPayload(const String& body) {
  ParseResult result = parseUsageJson(body, state);
  if (!result.ok) {
    Serial.print("Bad payload: ");
    Serial.println(result.error);
    state.mode = "error";
    state.status = "Bad JSON";
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("AI Desk Meter boot");

  state.status = "Booting";
  ui.begin();
  ui.render(state);

  wifi.begin(onPayload);
  state.mode = "pairing";
  state.status = "Waiting host";
}

void loop() {
  wifi.loop();
  ui.render(state);
  delay(250);
}
