import mysql.connector
import time
from datetime import datetime, timedelta
from db_connection import connect_to_database, close_connection
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from camera import detect_vehicles  # Importa la función desde camera.py

# Función para enviar correos
def send_email(to_email, subject, body, from_email, password, smtp_server, smtp_port):
    try:
        # Configurar el correo electrónico
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Asegurar la conexión
        server.login(from_email, password)

        # Enviar el correo
        server.sendmail(from_email, to_email, message.as_string())
        print(f"Correo enviado a {to_email}")

        # Cerrar la conexión con el servidor
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para verificar infracciones y registrar multas
def check_and_record_violation(carID, name, email, connection, processed_users, pending_violations):
    cursor = connection.cursor()
    try:
        thirty_minutes_ago = datetime.now() - timedelta(minutes=30)

        # Revisar si el usuario ya tiene una multa reciente en violation_history
        cursor.execute(""" 
            SELECT COUNT(*) FROM violation_history 
            WHERE carID = %s AND timestamp > %s
        """, (carID, thirty_minutes_ago))
        recent_violation_count = 0  # Inicializamos la variable

        row = cursor.fetchone()
        if row and isinstance(row[0], (int, float)):  
            recent_violation_count = int(row[0])

        # Revisar si el usuario tiene una multa en proceso en violations
        cursor.execute(""" 
            SELECT timestamp FROM violations 
            WHERE carID = %s
        """, (carID,))
        row = cursor.fetchone()
        active_violation = row[0] if row else None

        if recent_violation_count > 0 or active_violation:
            if carID not in processed_users:
                processed_users.add(carID)
                print(f"El usuario {carID} ya tiene una multa reciente o en proceso, no se registrará una nueva.")
            
            # Si la multa está en violations, esperar 30 segundos y verificar si sigue mal estacionado
            if active_violation:
                violation_time = active_violation
                if carID not in pending_violations:
                    pending_violations[carID] = violation_time
                    print(f"Esperando 30 segundos antes de mover la multa de {carID} a violation_history.")

            return

        # Revisar si el usuario está mal estacionado
        cursor.execute("SELECT parking_in, building FROM users WHERE carID = %s", (carID,))
        user_info = cursor.fetchone()

        if user_info:
            parking_in, building = user_info
            if parking_in == "Walker" and building != "Walker":
                current_time = datetime.now()
                violation_details = "Estacionado incorrectamente en Walker"

                # Registrar multa en violations
                cursor.execute("""
                    INSERT INTO violations (carID, timestamp, fine)
                    VALUES (%s, %s, %s)
                """, (carID, current_time.strftime("%Y-%m-%d %H:%M:%S"), violation_details))
                connection.commit()

                # Agregar a pending_violations inmediatamente
                pending_violations[carID] = current_time
                print(f"Multa registrada para {carID}: {violation_details}")
                print(f"Esperando 30 segundos antes de mover la multa de {carID} a violation_history.")

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")

    finally:
        cursor.close()

# Función para procesar las multas pendientes
def process_pending_violations(connection, pending_violations):
    """Mueve las multas de violations a violation_history si han pasado 30 segundos y envía un correo al usuario"""
    cursor = connection.cursor()
    try:
        current_time = datetime.now()
        to_remove = []

        for carID, violation_time in list(pending_violations.items()):
            if (current_time - violation_time).total_seconds() >= 30:
                # Mover la multa a violation_history
                cursor.execute("""
                    INSERT INTO violation_history (carID, timestamp, fine)
                    SELECT carID, NOW(), fine FROM violations WHERE carID = %s
                """, (carID,))
                connection.commit()

                # Obtener el email del usuario
                cursor.execute("SELECT email FROM users WHERE carID = %s", (carID,))
                user_email = cursor.fetchone()
                if user_email:
                    email = user_email[0]

                    # Crear el cuerpo del correo
                    subject = "Notificación de Multa de Tráfico"
                    body = f"""
                    Hola,

                    Este es un aviso sobre una infracción de tráfico reciente. Los detalles son los siguientes:

                    - ID de coche: {carID}
                    - Detalles de la infracción: Estacionado incorrectamente en Walker

                    Por favor, asegúrese de realizar el pago de la multa a la mayor brevedad posible.

                    Gracias,
                    Seguridad del Campus
                    """

                    # Enviar el correo al usuario
                    institution_email = "hernandezab@jbu.edu"  # Cambiar por tu email institucional
                    from_email = "BautistaI@jbu.edu"  # Cambiar por tu email
                    password = "Isbace26gokussj4"  # Cambiar por tu contraseña
                    smtp_server = "smtp.jbu.edu"
                    smtp_port = 587

                    send_email(email, subject, body, from_email, password, smtp_server, smtp_port)

                # Eliminar la multa de violations
                cursor.execute("DELETE FROM violations WHERE carID = %s", (carID,))
                connection.commit()

                print(f"Multa de {carID} movida a violation_history y eliminada de violations.")
                to_remove.append(carID)

        # Remover los procesados
        for carID in to_remove:
            pending_violations.pop(carID, None)

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")

    finally:
        cursor.close()

# Función principal
def main():
    connection = connect_to_database()
    if connection is None:
        print("No se pudo conectar a la base de datos. Saliendo del programa.")
        return

    processed_users = set()
    pending_violations = {}

    # Iniciar un hilo para la detección de vehículos
    detection_thread = threading.Thread(target=detect_vehicles)
    detection_thread.start()

    try:
        while True:
            cursor = connection.cursor()
            cursor.execute("SELECT carID, name, email FROM users")
            users = cursor.fetchall()
            cursor.close()

            for carID, name, email in users:
                check_and_record_violation(carID, name, email, connection, processed_users, pending_violations)

            # Procesar las multas pendientes
            process_pending_violations(connection, pending_violations)

            time.sleep(1)  # Esperar 1 segundo antes de la siguiente revisión

    except KeyboardInterrupt:
        print("\nDeteniendo el monitoreo de estacionamiento...")

    finally:
        close_connection(connection)

if __name__ == "__main__":
    print("Iniciando monitoreo de estacionamiento... (Presiona CTRL + C para detener)")
    main()
    print("Programa finalizado.")

