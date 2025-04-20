import cv2
import numpy as np
import serial
import time
import math

ser = serial.Serial('COM3', 9600)
time.sleep(2)

def send_cmd(cmd):
    ser.write(cmd.encode())
    print("Sent:", cmd)
    time.sleep(0.1)

# Red color range
low1 = np.array([0, 100, 100])
up1 = np.array([10, 255, 255])
low2 = np.array([160, 100, 100])
up2 = np.array([179, 255, 255])

goal = None
origin = None
goal_reached = False
last_cmd = ''
threshold_distance = 20

def set_goal(event, x, y, flags, param):
    global goal, goal_reached, origin
    if event == cv2.EVENT_LBUTTONDOWN:
        goal = (x, y)
        goal_reached = False
        origin = None  # Reset origin on new click
        print("Goal set to:", goal)

cv2.namedWindow("View")
cv2.setMouseCallback("View", set_goal)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Camera not found.")
    ser.close()
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, low1, up1)
    mask2 = cv2.inRange(hsv, low2, up2)
    mask = cv2.add(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx, cy = -1, -1

    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        if origin is None:
            origin = (cx, cy)  # Lock starting position
            print("Origin locked:", origin)

    if goal and origin and not goal_reached:
        gx, gy = goal
        ox, oy = origin
        dx = gx - ox
        dy = gy - oy
        target_angle = math.degrees(math.atan2(dy, dx))

        chair_dx = gx - cx
        chair_dy = gy - cy
        dist = math.hypot(chair_dx, chair_dy)

        heading_angle = math.degrees(math.atan2(chair_dy, chair_dx))

        angle_diff = target_angle - heading_angle
        angle_diff = (angle_diff + 180) % 360 - 180  # Normalize to [-180, 180]

        # Visuals
        cv2.circle(frame, goal, 5, (0, 0, 255), -1)
        cv2.line(frame, (cx, cy), goal, (255, 255, 0), 2)
        cv2.putText(frame, f"Dist: {int(dist)} Angle: {int(angle_diff)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Main control
        if dist < threshold_distance:
            send_cmd('S')
            goal_reached = True
            last_cmd = 'S'
        else:
            if angle_diff > 15:
                cmd = 'L'
            elif angle_diff < -15:
                cmd = 'R'
            else:
                cmd = 'f' if dist < 40 else 'F'

            if cmd != last_cmd:
                send_cmd(cmd)
                last_cmd = cmd

    elif goal_reached:
        cv2.putText(frame, "Goal Reached", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("View", frame)
    key = cv2.waitKey(1)
    if key == 27:
        send_cmd('S')
        break

cap.release()
cv2.destroyAllWindows()
ser.close()