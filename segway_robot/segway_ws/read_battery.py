import serial
import time

PORT = '/dev/ttyUSB0'
BAUD = 921600  # 🚀 Switched to high-speed Segway default

try:
    print(f"Connecting to Segway on {PORT} at {BAUD} baud...")
    ser = serial.Serial(PORT, BAUD, timeout=2) # Higher timeout
    time.sleep(1.0) # Let the port settle
    ser.reset_input_buffer()
    
    print("\n" + "="*40)
    print("🔋 SEGWAY TELEMETRY DIAGNOSTICS 🔋")
    print("="*40)

    # We will loop for 15 seconds to catch a reading
    end_time = time.time() + 15.0
    while time.time() < end_time:
        if ser.in_waiting > 0:
            # Read raw bytes and decode
            raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_data:
                print(f"📡 Received: {raw_data}")
        time.sleep(0.1)

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    print("\nDisconnected.")
