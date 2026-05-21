import serial
import time

port = '/dev/ttyUSB0'
baud = 115200

try:
    print(f"Connecting to Segway on {port}...")
    ser = serial.Serial(port, baud, timeout=1)
    
    # ⚠️ Check your surroundings before running!
    print("Nudging FORWARD for 2 seconds...")
    
    end_time = time.time() + 2.0
    while time.time() < end_time:
        # Send forward movement command (0.1 m/s speed, 0.0 rad/s turn)
        ser.write(b"RMP,0.1,0.0\r\n")
        time.sleep(0.05) # 20Hz loop

    print("Sending STOP command...")
    for _ in range(10):
        ser.write(b"RMP,0.0,0.0\r\n")
        time.sleep(0.05)

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    print("Done.")
