import time
import serial
import threading
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_connection import get_db_connection
from camera import detect_vehicles, capture_and_save_photo

# RFID Reader Configuration
RFID_PORT = "COM10"
BAUD_RATE = 9600

# Email Configuration
INSTITUTION_EMAIL = "BautistaI@jbu.edu"
FROM_EMAIL = "BautistaI@jbu.edu"
EMAIL_PASSWORD = "Gokussj4isbace"  
SMTP_SERVER = "smtp.jbu.edu"
SMTP_PORT = 587

pending_violations = {}

def send_email(to_email, subject, body):
    """Sends an email notification."""
    try:
        message = MIMEMultipart()
        message['From'] = FROM_EMAIL
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, message.as_string())

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Error sending email: {e}")

def check_and_record_violation(carID, name, email):
    """Checks and records parking violations."""
    connection = get_db_connection()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT timestamp FROM violations WHERE carID = %s", (carID,))
            if cursor.fetchone():
                print(f"User {carID} already has a pending violation.")
                return

            cursor.execute("SELECT parking_in, building FROM users WHERE carID = %s", (carID,))
            user_info = cursor.fetchone()

            if user_info:
                parking_in, building = user_info
                if parking_in == "Walker" and building != "Walker":
                    current_time = datetime.now()
                    violation_details = "Improperly parked in Walker"

                    cursor.execute("INSERT INTO violations (carID, timestamp, fine) VALUES (%s, %s, %s)",
                                   (carID, current_time, violation_details))
                    connection.commit()

                    pending_violations[carID] = current_time
                    print(f"Violation recorded for {carID}: {violation_details}")

                    # Send warning email after 1 minute
                    threading.Timer(60, send_warning_email, args=(carID, email)).start()

                    # Process final violation after 2 minutes
                    threading.Timer(120, process_final_violation, args=(carID, email)).start()

    except Exception as e:
        print(f"Database error: {e}")

    finally:
        connection.close()

def send_warning_email(carID, email):
    """Sends a warning if the vehicle has not been moved."""
    connection = get_db_connection()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT parking_in FROM users WHERE carID = %s", (carID,))
            parking_status = cursor.fetchone()

            if parking_status and parking_status[0] == "Walker":
                subject = "Warning: 1 minute to move your vehicle"
                body = f"""Hello,

You have 1 minute to move your vehicle before receiving a fine.

- Car ID: {carID}
- Violation: Improperly parked in Walker

If the vehicle remains in the same spot, a fine will be issued.

Thank you,  
Campus Security"""

                send_email(email, subject, body)

    except Exception as e:
        print(f"Database error: {e}")

    finally:
        connection.close()

def process_final_violation(carID, email):
    """Issues a fine if the vehicle has not been moved after 2 minutes."""
    connection = get_db_connection()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT parking_in FROM users WHERE carID = %s", (carID,))
            parking_status = cursor.fetchone()

            if parking_status and parking_status[0] == "Walker":
                cursor.execute("SELECT fine FROM violations WHERE carID = %s", (carID,))
                violation = cursor.fetchone()

                if violation:
                    fine_details = violation[0]

                    subject = "Violation Notification"
                    body = f"""Hello,

A fine has been issued for a traffic violation.

- Car ID: {carID}
- Violation Details: {fine_details}

Please make the necessary payment.

Thank you,  
Campus Security"""

                    send_email(email, subject, body)

                    cursor.execute("""
                        INSERT INTO violation_history (carID, timestamp, fine)
                        SELECT carID, NOW(), fine FROM violations WHERE carID = %s
                    """, (carID,))
                    connection.commit()

                    print(f"Fine processed and notification sent for {carID}.")

            else:
                print(f"Violation removed: {carID} moved the vehicle.")

            cursor.execute("DELETE FROM violations WHERE carID = %s", (carID,))
            connection.commit()
            pending_violations.pop(carID, None)

    except Exception as e:
        print(f"Database error: {e}")

    finally:
        connection.close()

def read_rfid():
    """Reads RFID tags and updates vehicle status in the database."""
    try:
        ser = serial.Serial(RFID_PORT, BAUD_RATE, timeout=1)
        print(f"Listening for RFID on {RFID_PORT}...")

        while True:
            if ser.in_waiting > 0:
                tag_data = ser.readline().decode('utf-8', errors='ignore').strip()
                tag_clean = tag_data.lstrip("\x02").replace("\r", "").replace("\n", "").upper()

                if not tag_clean or len(tag_clean) < 10:
                    continue  

                connection = get_db_connection()
                if not connection:
                    continue

                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT carID, name, email, parking_in FROM users WHERE rfid_tag = %s", (tag_clean,))
                        result = cursor.fetchone()

                        if result:
                            carID, name, email, parking_status = result
                            new_status = "Walker" if parking_status in (None, "none") else "none"

                            capture_and_save_photo(carID)

                            cursor.execute("UPDATE users SET parking_in = %s WHERE rfid_tag = %s", (new_status, tag_clean))
                            connection.commit()

                            print(f"{name} updated to: {new_status}")

                            check_and_record_violation(carID, name, email)

                        else:
                            print(f"Tag '{tag_clean}' not registered.")

                except Exception as e:
                    print(f"Database error: {e}")

                finally:
                    connection.close()

    except serial.SerialException as e:
        print(f"Serial port error: {e}")

def main():
    threading.Thread(target=read_rfid, daemon=True).start()
    threading.Thread(target=detect_vehicles, daemon=True).start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping monitoring system...")

if __name__ == "__main__":
    print("Monitoring system running... (Press CTRL + C to stop)")
    main()

