import serial
import mysql.connector
from datetime import datetime

# MySQL Database Configuration
DB_CONFIG = {'host': 'localhost','user': 'root','password': '','database': 'vcd'}

def insert_into_db(gate, action):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        timestamp = datetime.now()
        
        query = """
        INSERT INTO dashboard_carlog(gate, action, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (gate, action, timestamp, timestamp))
        conn.commit()
        print(f"Inserted: Gate {gate}, Action {action}, Timestamp {timestamp}")
    
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    
    finally:
        cursor.close()
        conn.close()

SERIAL_PORT = "COM4"
BAUD_RATE = 9600

def read_serial():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT}...")
    
    while True:
        data = ser.read(5)  # Read 5 bytes
        if len(data) == 5 and data[0] == 0xAA and data[4] == 0x55:
            gate = data[1]
            action = "entry" if data[2:4] == b'\x01\x00' else "exit"
            insert_into_db(gate, action)
        
if __name__ == "__main__":
    read_serial()
