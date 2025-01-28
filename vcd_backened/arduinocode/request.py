import datetime
import mysql.connector
import time

LOG_FILE = "connection_log.txt"

db_config = { 'host': 'localhost', 'user': 'root', 'password': 'password','database': 'paytm_anpr'}

def log_message(message):
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp}: {message}\n")

def check_exit_boom():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT exitboom FROM boomsig"
        cursor.execute(query)

        result = cursor.fetchone()
        if result:
            exit_boom_status = result[0]
            if exit_boom_status == 'Y':
                log_message("Exit boom is open")
                # Perform actions here when the exit boom is open
                time.sleep(3)  # Wait for 3 seconds
                cursor.execute("UPDATE boomsig SET exitboom = 'N'")
                conn.commit()
                log_message("Exit boom status reset to 'N' after 3 seconds")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        log_message(f"Error: {err}")

def main():
    while True:
        check_exit_boom()
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()

'''


'''
