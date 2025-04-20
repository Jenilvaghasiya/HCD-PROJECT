import RPi.GPIO as GPIO
import time
import pigpio  # For smooth servo movement

GPIO.setmode(GPIO.BCM)

# Ultrasonic GPIO setup
ultrasonics = [
    {'trig': 17, 'echo': 27},
    {'trig': 22, 'echo': 23},
    {'trig': 5,  'echo': 6},
    {'trig': 13, 'echo': 19}
]

for us in ultrasonics:
    GPIO.setup(us['trig'], GPIO.OUT)
    GPIO.setup(us['echo'], GPIO.IN)

# Servo setup
pi = pigpio.pi()
servo_pins = [12, 16, 20, 21]

for pin in servo_pins:
    pi.set_mode(pin, pigpio.OUTPUT)

# Function to measure distance
def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm
    return round(distance, 2)

# Function to move servo
def set_servo_angle(pin, angle):
    duty = int((500 + (angle * 2000 / 180)))  # Convert angle to pulse width
    pi.set_servo_pulsewidth(pin, duty)

# Example usage
try:
    while True:
        for i, us in enumerate(ultrasonics):
            dist = get_distance(us['trig'], us['echo'])
            print(f"Sensor {i+1}: {dist} cm")
            time.sleep(0.1)

        set_servo_angle(12, 90)
        time.sleep(1)
        set_servo_angle(12, 0)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    pi.stop()
