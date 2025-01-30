import socket
import datetime
import time
import mysql.connector
import threading
import re

SERVER_IP = "192.168.1.157"
SERVER_PORT = 7000

# Database Configuration
DB_CONFIG = {"host": "localhost","user": "root","password": "","database": "vcd"}

LOG_FILE = "Entry_Boom_services.txt"
INITIAL_MESSAGE = "|OPENEN%"

def log_message(message):
    """Logs messages to a file with timestamps."""
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp}: {message}\n")

def send_message(client_socket, message):
    """Sends a message through the socket."""
    try:
        client_socket.sendall(message.encode())
        log_message(f"Sent message: {message}")
    except Exception as e:
        log_message(f"Failed to send message: {e}")

def check_exit_boom(client_socket):
    """Checks database for exit boom status and sends a message if needed."""
    last_status = None
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("SELECT entryboom FROM boomsig")
            result = cursor.fetchone()  # Fetch one row
            
            # Make sure to consume all results
            cursor.fetchall()  # This ensures that any remaining results are consumed

            if result:
                exit_boom_status = result[0]
                if exit_boom_status == 'Y':
                    log_message("Exit boom is open")
                    send_message(client_socket, INITIAL_MESSAGE)
                    cursor.execute("UPDATE boomsig SET entryboom = 'N' WHERE id = 1")
                    conn.commit()
                    log_message("Successfully updated entryboom to 'N'")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            log_message(f"Database error: {err}")
        except Exception as e:
            log_message(f"Unexpected error: {e}")
        time.sleep(3)  # Check every 3 seconds


def insert_gate_action(gate, action):
    """Inserts the received gate number and action into the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dashboard_carlog (gate, action) VALUES (%s, %s)", (gate, action))
        conn.commit()
        cursor.close()
        conn.close()
        log_message(f"Inserted into DB: Gate {gate}, Action {action}")
    except mysql.connector.Error as err:
        log_message(f"Database error: {err}")
        
def main():
    """Main function to establish socket connection and start monitoring."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        log_message(f"Connected to {SERVER_IP}:{SERVER_PORT}")

        # Start database monitoring in a separate thread
        thread = threading.Thread(target=check_exit_boom, args=(client_socket,), daemon=True)
        thread.start()
        
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("Connection lost. Reconnecting...")
                    break

                buffer += data.decode('utf-8')

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    print(f"Received: {line}")

                    if "|HLT%" in line:
                        print(f"Received health packet: {line}")

                    match = re.search(r'(\d+)\s+(\w+)', line)
                    if match:
                        gate_number, action = match.groups()
                        insert_gate_action(gate_number, action)

                time.sleep(1)

            except socket.error as e:
                log_message(f"Socket error: {e}")
                break

    except Exception as e:
        log_message(f"Connection error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
