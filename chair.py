import time
import random
import math

# Simulated Components
class SimulatedLidar:
    def map_room(self, room_radius):
        print("Scanning room with LiDAR...")
        time.sleep(5)  # Simulate scanning delay
        print(f"Room mapping complete. Room radius: {room_radius}cm")
        return room_radius

class SimulatedUltrasonic:
    @staticmethod
    def get_distance():
        return random.randint(10, 300)  # Simulating obstacle detection

class SimulatedWheels:
    @staticmethod
    def move_forward():
        print("Moving forward...")
        time.sleep(1.5)

    @staticmethod
    def move_backward():
        print("Moving backward...")
        time.sleep(1.5)

    @staticmethod
    def move_left():
        print("Moving left...")
        time.sleep(1.5)

    @staticmethod
    def move_right():
        print("Moving right...")
        time.sleep(1.5)

    @staticmethod
    def rotate_to(angle):
        print(f"Rotating to {angle} degrees...")
        time.sleep(2)

# Simulated Setup
lidar = SimulatedLidar()
ultrasonic = SimulatedUltrasonic()
wheels = SimulatedWheels()

# Chair Positioning System
class Chair:
    def _init_(self, room_radius, path):
        self.room_radius = room_radius
        self.path = path  # Predefined path [(x1, y1), (x2, y2), ..., (home_x, home_y)]
        self.position = path[0]  # Starting position

    def scan_room(self):
        self.room_radius = lidar.map_room(self.room_radius)
        time.sleep(10)  # Pause before moving

    def detect_obstacle(self):
        return ultrasonic.get_distance() < 50  # If distance < 50cm, consider it an obstacle

    def move_to(self, target_x, target_y):
        print(f"Moving towards ({target_x}, {target_y})...")
        while math.dist(self.position, (target_x, target_y)) > 5:
            if self.detect_obstacle():
                print("Obstacle detected! Adjusting route...")
                wheels.move_right()
                time.sleep(2)  # Slower adjustment
            else:
                # Move in the required direction
                if self.position[0] < target_x:
                    wheels.move_right()
                    self.position = (self.position[0] + 7, self.position[1])
                elif self.position[0] > target_x:
                    wheels.move_left()
                    self.position = (self.position[0] - 7, self.position[1])

                if self.position[1] < target_y:
                    wheels.move_forward()
                    self.position = (self.position[0], self.position[1] + 7)
                elif self.position[1] > target_y:
                    wheels.move_backward()
                    self.position = (self.position[0], self.position[1] - 7)

                time.sleep(2)  # Slower movement for a longer duration
        print(f"Reached ({target_x}, {target_y})")

    def follow_path(self):
        print("Following predefined path...")
        for waypoint in self.path[1:]:  # Skip the first since it's the starting position
            self.move_to(*waypoint)

    def start(self):
        print("Starting chair positioning system...")
        self.scan_room()
        self.follow_path()
        print("Chair is successfully placed at its home position!")

# Example Simulation
room_radius = 100  # Example room radius
predefined_path = [(40, 40), (30, 50), (25, 40), (25, 25)]  # Given path to follow

chair = Chair(room_radius, predefined_path)
chair.start()
