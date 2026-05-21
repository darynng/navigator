import serial
import sys
import tty
import termios
import time

# --- Configuration ---
PORT = '/dev/ttyUSB0'
BAUD = 115200

# Speeds
LINEAR_SPEED = 0.50   # Meters per second (Forward/Backward)
ANGULAR_SPEED = 0.5   # Radians per second (Turning)

def getch():
    """Gets a single character from standard input without needing Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    try:
        print(f"Connecting to Segway on {PORT}...")
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print("✅ Connected!")
        
        print("\n" + "="*40)
        print("🎮 SEGWAY KEYBOARD TELEOP ACTIVE 🎮")
        print("="*40)
        print("  W : Forward")
        print("  S : Backward")
        print("  A : Turn Left")
        print("  D : Turn Right")
        print("  Spacebar : STOP")
        print("  Q : Quit Script")
        print("="*40)

# --- 🆕 ADD THIS: SET THE CHASSIS TO TRACTOR MODE (GREEN LIGHT) ---
        print("🔓 Unlocking Chassis (Sending Tractor Mode Command)...")
        ser.write(b"RMP_SET_MODE,1\r\n") # This is the standard unlock string
        time.sleep(0.5)

        current_linear = 0.0
        current_angular = 0.0

        print("🎮 Driving Mode Active! Press W/A/S/D to move, Space to stop.")

        while True:
            # We use a non-blocking key check here (or just use your previous getch)
            key = getch() 

            if key.lower() == 'w': current_linear = 0.3; current_angular = 0.0
            elif key.lower() == 's': current_linear = -0.3; current_angular = 0.0
            elif key.lower() == 'a': current_linear = 0.0; current_angular = 0.3
            elif key.lower() == 'd': current_linear = 0.0; current_angular = -0.3
            elif key == ' ': current_linear = 0.0; current_angular = 0.0
            elif key.lower() == 'q': break

            # 🔥 THE HEARTBEAT: Send the command repeatedly to satisfy the Segway watchdog
            command = f"RMP,{current_linear},{current_angular}\r\n".encode()
            ser.write(command)
            time.sleep(0.02) # 50Hz frequency (Required for RMP 401)

            time.sleep(0.05) # Small debounce delay

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            # Always send a stop command on exit!
            ser.write(b"RMP,0.0,0.0\r\n")
            ser.close()
            print("Serial port closed safely.")

if __name__ == "__main__":
    main()
