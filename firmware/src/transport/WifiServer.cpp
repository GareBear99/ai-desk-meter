#include "WifiServer.h"

void WifiServerTransport::begin(PayloadCallback cb) {
  callback = cb;
  // TODO: implement Wi-Fi AP/STA and HTTP POST /api/state.
  // Kept as a placeholder so the repo compiles after board-specific networking is selected.
  Serial.println("WifiServerTransport placeholder ready");
}

void WifiServerTransport::loop() {
  // TODO: handle HTTP clients or WebSocket messages.
}
