from rplidar import RPLidar
import threading

# Set correct USB ports (check using `ls /dev/ttyUSB*` on Raspberry Pi)
PORT1 = '/dev/ttyUSB0'
PORT2 = '/dev/ttyUSB1'

lidar1 = RPLidar(PORT1)
lidar2 = RPLidar(PORT2)

def read_lidar_data(lidar, name):
    try:
        for scan in lidar.iter_scans(max_buf_meas=500):
            print(f"--- {name} Data ---")
            for (_, angle, distance) in scan:
                print(f"{name} Angle: {angle:.2f}°, Distance: {distance:.2f} mm")
    except KeyboardInterrupt:
        print(f"{name} stopped.")
        lidar.stop()
        lidar.disconnect()

# Use threading to read from both sensors simultaneously
thread1 = threading.Thread(target=read_lidar_data, args=(lidar1, 'LIDAR1'))
thread2 = threading.Thread(target=read_lidar_data, args=(lidar2, 'LIDAR2'))

thread1.start()
thread2.start()
