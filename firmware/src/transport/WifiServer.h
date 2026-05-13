#pragma once
#include <Arduino.h>
#include <functional>

using PayloadCallback = std::function<void(const String&)>;

class WifiServerTransport {
public:
  void begin(PayloadCallback cb);
  void loop();
private:
  PayloadCallback callback;
};
