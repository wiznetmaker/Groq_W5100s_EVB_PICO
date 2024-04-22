# How to Get an Answer to RP2040 in 4 Seconds with Groq

This project demonstrates using Groq's innovative LPU chip and Meta's LLaMA3 model to achieve fast response times with the RP2040 microcontroller, ideal for AIoT applications.

## Project Overview

Utilizing the cutting-edge technology from Groq and Meta, this project aims to replace traditional response mechanisms on the maker site with a much faster and efficient alternative using the RP2040 connected to Groq's cloud services.

## Hardware Components

- **WIZnet - W5100S-EVB-Pico x 1**

## Software and Libraries

- MicroPython
- Groq API
- Other dependencies listed in `requirements.txt`

## Setup Instructions

1. **GroqCloud Setup**
   - Visit the [Groq Cloud homepage](https://api.groq.com/openai/v1/chat/completions).
   - Sign up and obtain your API KEY.
   - Ensure the Groq library is installed (not applicable directly on Pico, use API communication).

2. **Ethernet Initialization**
   - Use the following MicroPython code to initialize your Ethernet connection via WIZnet hardware:
   ```python
   from machine import Pin, SPI
   import network
   import utime

   def init_ethernet(timeout=10):
       spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
       nic = network.WIZNET5K(spi, Pin(17), Pin(20))
       nic.active(True)
       start_time = utime.ticks_ms()
       while not nic.isconnected():
           if (utime.ticks_diff(utime.ticks_ms(), start_time) > timeout * 1000):
               raise Exception("Ethernet connection timed out.")
           utime.sleep(1)
       print('Ethernet connected. IP:', nic.ifconfig())
