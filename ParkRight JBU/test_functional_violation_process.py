import pytest
import mysql.connector
from datetime import datetime, timedelta
from db_connection import connect_to_database, close_connection
from violation_process_2 import check_and_record_violation, process_pending_violations, send_email

@pytest.fixture
def real_database_connection():
    """Establece una conexión real con la base de datos para pruebas funcionales."""
    connection = connect_to_database()
    if connection is None:
        pytest.fail("No se pudo conectar a la base de datos real.")
    yield connection
    close_connection(connection)

def test_functional_violation_process(real_database_connection):
    """Prueba funcional: verifica que una multa se registre y se mueva a violation_history."""
    connection = real_database_connection
    cursor = connection.cursor()

    # Datos de prueba
    carID = "RFID_TEST_001"
    name = "Test User"
    email = "testuser@email.com"

    # Asegurar que el usuario existe en la tabla users
    cursor.execute("DELETE FROM users WHERE carID = %s", (carID,))
    cursor.execute("INSERT INTO users (carID, name, email, parking_in, building) VALUES (%s, %s, %s, %s, %s)",
                   (carID, name, email, "Walker", "Engineering"))
    connection.commit()

    # Conjuntos de seguimiento
    processed_users = set()
    pending_violations = {}

    # **Paso 1:** Registrar la multa
    check_and_record_violation(carID, name, email, connection, processed_users, pending_violations)

    # **Paso 2:** Verificar que la multa se guardó en violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 1, "La multa no se registró correctamente en violations"

    # **Paso 3:** Simular espera de 30 segundos y procesar multas
    pending_violations[carID] = datetime.now() - timedelta(seconds=35)
    process_pending_violations(connection, pending_violations)

    # **Paso 4:** Verificar que la multa pasó a violation_history
    cursor.execute("SELECT COUNT(*) FROM violation_history WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 1, "La multa no se movió a violation_history correctamente"

    # **Paso 5:** Verificar que la multa fue eliminada de violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 0, "La multa no fue eliminada de violations"

    # **Paso 6:** Verificar que se envió el correo (solo se muestra en la consola)
    print(f"✅ Correo enviado a {email} notificando la multa.")

    # **Limpieza:** Eliminar datos de prueba
    cursor.execute("DELETE FROM users WHERE carID = %s", (carID,))
    cursor.execute("DELETE FROM violation_history WHERE carID = %s", (carID,))
    connection.commit()
    cursor.close()

def test_functional_pending_violations(real_database_connection):
    """Prueba funcional: Manejo de multas pendientes."""
    connection = real_database_connection
    cursor = connection.cursor()

    # Datos de prueba
    carID = "RFID_PENDING_001"
    email = "pendinguser@email.com"

    # Asegurar que el usuario existe en la tabla users
    cursor.execute("DELETE FROM users WHERE carID = %s", (carID,))
    cursor.execute("INSERT INTO users (carID, email, parking_in, building) VALUES (%s, %s, %s, %s)",
                   (carID, email, "Walker", "Engineering"))
    connection.commit()

    # **Paso 1:** Registrar la multa
    check_and_record_violation(carID, "Test User", email, connection, set(), {})

    # **Paso 2:** Verificar que la multa se guardó en violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 1, "La multa no se registró correctamente en violations"

    # **Paso 3:** Simular que la multa está pendiente (más de 30 segundos)
    pending_violations = {carID: datetime.now() - timedelta(seconds=35)}

    # **Paso 4:** Procesar las multas pendientes
    process_pending_violations(connection, pending_violations)

    # **Paso 5:** Verificar que la multa pasó a violation_history
    cursor.execute("SELECT COUNT(*) FROM violation_history WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 1, "La multa no se movió a violation_history correctamente"

    # **Paso 6:** Verificar que la multa fue eliminada de violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", (carID,))
    assert cursor.fetchone()[0] == 0, "La multa no fue eliminada de violations"

    # **Paso 7:** Verificar que se envió el correo (solo se muestra en la consola)
    print(f"✅ Correo enviado a {email} notificando la multa.")

    # **Limpieza:** Eliminar datos de prueba
    cursor.execute("DELETE FROM users WHERE carID = %s", (carID,))
    cursor.execute("DELETE FROM violation_history WHERE carID = %s", (carID,))
    connection.commit()
    cursor.close()

def test_functional_invalid_user_data(real_database_connection):
    """Prueba funcional: Manejo de datos de usuario inválidos."""
    connection = real_database_connection
    cursor = connection.cursor()

    # Datos de prueba con car ID y email inválidos
    invalid_carID = "INVALID_CAR_ID"
    invalid_email = "invalidemail.com"

    # **Paso 1:** Intentar registrar una multa con un carID inválido
    check_and_record_violation(invalid_carID, "Invalid User", invalid_email, connection, set(), {})

    # **Paso 2:** Verificar que no se ha agregado ninguna multa a la tabla violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", (invalid_carID,))
    assert cursor.fetchone()[0] == 0, "La multa debería haber sido rechazada debido al carID inválido."

    # **Paso 3:** Intentar registrar una multa con un email inválido
    check_and_record_violation("RFID_TEST_001", "Invalid User", invalid_email, connection, set(), {})

    # **Paso 4:** Verificar que no se ha agregado ninguna multa a la tabla violations
    cursor.execute("SELECT COUNT(*) FROM violations WHERE carID = %s", ("RFID_TEST_001",))
    assert cursor.fetchone()[0] == 0, "La multa debería haber sido rechazada debido al email inválido."

    # **Limpieza:** No es necesario eliminar datos ya que no se registraron violaciones

    cursor.close()



