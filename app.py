import time
import math
import random
from gpiozero import Motor, DistanceSensor

# Simulated Room Configuration
tables = [(1, 0.5, 0.5), (2, 2.5, 0.5)]  # (Table ID, X, Y)
obstacles = [(1.5, 1.5), (2.0, 2.0)]  # Obstacle Positions

# Motor and Sensor Setup for Chair 1
motor1_left = Motor(forward=17, backward=18)
motor1_right = Motor(forward=22, backward=23)
sensor1 = DistanceSensor(echo=24, trigger=25)

# Motor and Sensor Setup for Chair 2
motor2_left = Motor(forward=5, backward=6)
motor2_right = Motor(forward=12, backward=13)
sensor2 = DistanceSensor(echo=19, trigger=26)

class SmartChair:
    def __init__(self, chair_id, motor_left, motor_right, sensor, x_start, y_start):
        self.chair_id = chair_id
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.sensor = sensor
        self.x, self.y = x_start, y_start
        self.destination = None

    def find_nearest_table(self):
        min_distance = float("inf")
        nearest_table = None
        for table_id, tx, ty in tables:
            distance = math.sqrt((self.x - tx) ** 2 + (self.y - ty) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_table = (tx, ty)
        self.destination = nearest_table

    def move_forward(self, duration=1):
        self.motor_left.forward()
        self.motor_right.forward()
        time.sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def move_backward(self, duration=1):
        self.motor_left.backward()
        self.motor_right.backward()
        time.sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def turn_left(self, duration=0.5):
        self.motor_left.backward()
        self.motor_right.forward()
        time.sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def turn_right(self, duration=0.5):
        self.motor_left.forward()
        self.motor_right.backward()
        time.sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def detect_obstacle(self):
        return self.sensor.distance < 0.3  # 30 cm obstacle detection

    def navigate_to_table(self):
        self.find_nearest_table()
        if not self.destination:
            print(f"Chair {self.chair_id}: No destination found!")
            return

        tx, ty = self.destination
        print(f"Chair {self.chair_id} moving to Table at {tx}, {ty}")

        while True:
            if self.detect_obstacle():
                print(f"Chair {self.chair_id} detected an obstacle! Adjusting path...")
                self.turn_left(random.uniform(0.5, 1.5))
                self.move_forward(0.5)
                self.turn_right(random.uniform(0.5, 1.5))
            else:
                self.move_forward(1)
                self.x += 0.1  # Simulated movement
                self.y += 0.1

            if math.sqrt((self.x - tx) ** 2 + (self.y - ty) ** 2) < 0.2:
                print(f"Chair {self.chair_id} reached Table at {tx}, {ty}")
                break

# Initialize chairs
chair1 = SmartChair(1, motor1_left, motor1_right, sensor1, 2.0, 3.0)
chair2 = SmartChair(2, motor2_left, motor2_right, sensor2, 3.0, 1.0)

# Move chairs to their assigned tables
chair1.navigate_to_table()
chair2.navigate_to_table()
