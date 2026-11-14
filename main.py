import socket
import json
import sys
import numpy as np
from sklearn.linear_model import LinearRegression

# Simulated historical training data for indoor ferns:
# Features: [Temperature (°C), Humidity (%)]
# Target: Days until next watering
X_train = np.array([
    [22.0, 65.0],
    [24.5, 50.0],
    [28.0, 40.0],
    [20.0, 80.0],
    [26.0, 45.0],
    [21.5, 70.0],
    [29.0, 35.0],
    [23.0, 60.0]
])
y_train = np.array([5, 3, 2, 7, 3, 6, 2, 4])

def train_model():
    """Trains and returns a Linear Regression model on historical sensor records."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def handle_socket_sensor_feed(model, host='127.0.0.1', port=65432):
    """Starts a local socket server to ingest sensor data packets."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[*] Socket server listening on {host}:{port}...")
        print("[*] Send a JSON payload via socket or use terminal input below.")
    except Exception as e:
        print(f"[!] Socket binding error: {e}")
        return

    # For demonstration, we handle one connection or fallback to interactive terminal
    server_socket.settimeout(2.0)
    try:
        conn, addr = server_socket.accept()
        with conn:
            print(f"[+] Connected by sensor node: {addr}")
            data = conn.recv(1024)
            if data:
                payload = json.loads(data.decode('utf-8'))
                temp = float(payload.get('temperature'))
                humidity = float(payload.get('humidity'))
                prediction = model.predict([[temp, humidity]])[0]
                print(f"[+] Sensor Data Received -> Temp: {temp}°C | Humidity: {humidity}%")
                print(f"[+] Estimated days until watering: {max(1, round(prediction, 1))} days")
    except socket.timeout:
        print("[-] No incoming socket connection detected within timeout. Switching to terminal input mode.")
    finally:
        server_socket.close()

def get_user_terminal_input():
    """Takes dynamic ambient records from the user in the terminal."""
    print("\n--- Interactive Fern Watering Prediction ---")
    try:
        temp_input = input("Enter current room temperature (°C, e.g., 25.5): ").strip()
        humidity_input = input("Enter current room humidity (%, e.g., 48.0): ").strip()
        
        temperature = float(temp_input)
        humidity = float(humidity_input)
        
        if not (-10 <= temperature <= 60) or not (0 <= humidity <= 100):
            raise ValueError("Sensor values out of realistic household range.")
            
        return temperature, humidity
    except ValueError as err:
        print(f"[!] Invalid input: {err}. Please enter valid numerical values.")
        sys.exit(1)

def main():
    model = train_model()
    
    # Optional socket data ingestion check
    handle_socket_sensor_feed(model)
    
    # Mandatory terminal input execution for dynamic runtime results
    temp, humidity = get_user_terminal_input()
    
    # Predict watering interval
    predicted_days = model.predict([[temp, humidity]])[0]
    safe_days = max(1.0, round(predicted_days, 1))
    
    print("\n----------------------------------------")
    print(f" Room Temperature : {temp}°C")
    print(f" Room Humidity    : {humidity}%")
    print(f" Prediction       : Water your indoor fern in approx. **{safe_days} days**.")
    print("----------------------------------------")

if __name__ == "__main__":
    main()