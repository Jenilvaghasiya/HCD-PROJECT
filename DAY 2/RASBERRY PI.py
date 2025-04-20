import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
LED_PIN = 17  # GPIO 17 (physical pin 11)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

print("Blinking LED. Press CTRL+C to stop.")

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        time.sleep(1)  # Wait 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        time.sleep(1)  # Wait 1 second

except KeyboardInterrupt:
    print("\nProgram stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO pins
