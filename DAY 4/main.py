import cv2
import numpy as np
import serial
import time
import math

# Serial communication
ser = serial.Serial('COM3', 9600)
time.sleep(2)

def send_cmd(cmd):
    ser.write(cmd.encode())
    print("Sent:", cmd)
    time.sleep(0.1)

# HSV for red detection
low1 = np.array([0, 100, 100])
up1 = np.array([10, 255, 255])
low2 = np.array([160, 100, 100])
up2 = np.array([179, 255, 255])

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Camera not found")
    ser.close()
    exit()

home = None
going_home = False

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect red marker (chair)
    mask1 = cv2.inRange(hsv, low1, up1)
    mask2 = cv2.inRange(hsv, low2, up2)
    mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx, cy = -1, -1

    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    if home and cx != -1:
        hx, hy = home
        dx = hx - cx
        dy = hy - cy
        distance = math.hypot(dx, dy)

        cv2.circle(frame, home, 5, (0, 0, 255), -1)
        cv2.line(frame, (cx, cy), home, (255, 255, 0), 2)

        if going_home:
            print(f"Chair: ({cx},{cy})  Home: ({hx},{hy})  Distance: {distance:.2f}")

            if distance < 30:
                send_cmd('S')
                going_home = False
            else:
                # Simple movement: always move forward
                send_cmd('F')

    cv2.putText(frame, "Press 'm' to mark, 'r' to return", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Chair Navigation", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        send_cmd('S')
        break
    elif key == ord('m') and cx != -1:
        home = (cx, cy)
        print("Home marked at:", home)
    elif key == ord('r') and home:
        print("Returning to home...")
        going_home = True

cap.release()
cv2.destroyAllWindows()
ser.close()