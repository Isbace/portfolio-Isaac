import mysql.connector
import time
import serial
from datetime import datetime, timedelta
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_connection import connect_to_database, close_connection
from camera import detect_vehicles  # Función de detección de vehículos

# Configuración de puerto RFID
RFID_PORT = "COM10"
BAUD_RATE = 9600

# Configuración del correo
INSTITUTION_EMAIL = "hernandezab@jbu.edu"
FROM_EMAIL = "BautistaI@jbu.edu"
EMAIL_PASSWORD = "Isbace26gokussj4"  # Cambiar por tu contraseña
SMTP_SERVER = "smtp.jbu.edu"
SMTP_PORT = 587

# Diccionario para multas pendientes
pending_violations = {}

# Conectar a la base de datos
connection = connect_to_database()
if connection is None:
    print("No se pudo conectar a la base de datos.")
    exit()

# Función para enviar correos
def send_email(to_email, subject, body):
    try:
        message = MIMEMultipart()
        message['From'] = FROM_EMAIL
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, message.as_string())
        server.quit()

        print(f"Correo enviado a {to_email}")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para verificar infracciones y registrar multas
def check_and_record_violation(carID, name, email):
    cursor = connection.cursor()
    try:
        thirty_minutes_ago = datetime.now() - timedelta(minutes=30)

        # Verificar multas recientes en violation_history
        cursor.execute("""
            SELECT COUNT(*) FROM violation_history 
            WHERE carID = %s AND timestamp > %s
        """, (carID, thirty_minutes_ago))
        recent_violation_count = cursor.fetchone()[0]

        # Verificar multas activas en violations
        cursor.execute("SELECT timestamp FROM violations WHERE carID = %s", (carID,))
        active_violation = cursor.fetchone()

        if recent_violation_count > 0 or active_violation:
            print(f"El usuario {carID} ya tiene una multa reciente o en proceso.")
            return

        # Verificar si está mal estacionado
        cursor.execute("SELECT parking_in, building FROM users WHERE carID = %s", (carID,))
        user_info = cursor.fetchone()

        if user_info:
            parking_in, building = user_info
            if parking_in == "Walker" and building != "Walker":
                current_time = datetime.now()
                violation_details = "Estacionado incorrectamente en Walker"

                # Registrar multa en violations
                cursor.execute("INSERT INTO violations (carID, timestamp, fine) VALUES (%s, %s, %s)",
                               (carID, current_time, violation_details))
                connection.commit()

                pending_violations[carID] = current_time
                print(f"Multa registrada para {carID}: {violation_details}")

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        cursor.close()

# Función para procesar multas pendientes
def process_pending_violations():
    cursor = connection.cursor()
    try:
        current_time = datetime.now()
        to_remove = []

        for carID, violation_time in list(pending_violations.items()):
            elapsed_time = (current_time - violation_time).total_seconds()

            if elapsed_time >= 30:
                # Verificar si la multa aún está en violations
                cursor.execute("SELECT fine FROM violations WHERE carID = %s", (carID,))
                violation = cursor.fetchone()

                if violation:
                    fine_details = violation[0]

                    # Obtener email del usuario
                    cursor.execute("SELECT email FROM users WHERE carID = %s", (carID,))
                    user_email = cursor.fetchone()

                    if user_email:
                        email = user_email[0]
                        subject = "Notificación de Multa de Tráfico"
                        body = f"""Hola,

Este es un aviso sobre una infracción de tráfico reciente.

- ID de coche: {carID}
- Detalles de la infracción: {fine_details}

Por favor, asegúrese de realizar el pago de la multa.

Gracias,
Seguridad del Campus"""

                        send_email(email, subject, body)

                    # Si se procesó la multa, mover a violation_history
                    cursor.execute("""
                        INSERT INTO violation_history (carID, timestamp, fine)
                        SELECT carID, NOW(), fine FROM violations WHERE carID = %s
                    """, (carID,))
                    connection.commit()

                    print(f"Multa de {carID} procesada y notificada.")

                else:
                    print(f"Multa de {carID} eliminada sin procesar.")

                # Eliminar la multa de violations y del diccionario
                cursor.execute("DELETE FROM violations WHERE carID = %s", (carID,))
                connection.commit()

                to_remove.append(carID)

        for carID in to_remove:
            pending_violations.pop(carID, None)

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        cursor.close()

# Función para leer tarjetas RFID y actualizar la base de datos
def read_rfid():
    try:
        ser = serial.Serial(RFID_PORT, BAUD_RATE, timeout=1)
        print(f"Escuchando RFID en {RFID_PORT}...")

        while True:
            if ser.in_waiting > 0:
                tag_data = ser.readline()
                tag_clean = tag_data.decode('utf-8', errors='ignore').strip()
                tag_clean = tag_clean.lstrip("\x02").replace("\r", "").replace("\n", "").upper()

                if not tag_clean or len(tag_clean) < 10:
                    continue  

                cursor = connection.cursor()
                cursor.execute("SELECT carID, name, email, parking_in FROM users WHERE rfid_tag = %s", (tag_clean,))
                result = cursor.fetchone()

                if result:
                    carID, name, email, parking_status = result
                    new_status = "Walker" if parking_status in (None, "none") else "none"

                    cursor.execute("UPDATE users SET parking_in = %s WHERE rfid_tag = %s", (new_status, tag_clean))
                    connection.commit()

                    

                    # Verificar si el usuario merece una multa
                    check_and_record_violation(carID, name, email)

                else:
                    print(f"Tag '{tag_clean}' no registrado en la base de datos.")

                cursor.close()

    except serial.SerialException as e:
        print(f"Error en el puerto serial: {e}")

# Función principal
def main():
    # Hilo para lectura de RFID
    rfid_thread = threading.Thread(target=read_rfid)
    rfid_thread.start()

    # Hilo para detección de vehículos
    detection_thread = threading.Thread(target=detect_vehicles)
    detection_thread.start()

    try:
        while True:
            process_pending_violations()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDeteniendo el monitoreo...")

    finally:
        close_connection(connection)

if __name__ == "__main__":
    print("Sistema de monitoreo en ejecución... (Presiona CTRL + C para detener)")
    main()
