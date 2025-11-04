import pytest
from datetime import datetime, timedelta
import violation_process_2 

@pytest.fixture
def mock_connection(mocker):
    """Simula la conexión a la base de datos."""
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

def test_check_and_record_violation(mock_connection, mocker):
    """Verifica que se registre una multa si un auto está mal estacionado"""
    mock_conn, mock_cursor = mock_connection
    processed_users = set()
    pending_violations = {}

    # Simulamos respuestas de la base de datos
    mock_cursor.fetchone.side_effect = [
        (0,),  # No tiene multas recientes en violation_history
        None,  # No tiene multas activas en violations
        ("Walker", "Engineering")  # Está mal estacionado (debería recibir multa)
    ]

    violation_process_2.check_and_record_violation(
        "RFID_123", "Juan", "juan@email.com", mock_conn, processed_users, pending_violations
    )

    # Verificar que se registró una multa en violations
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list] 
    #Esto limpia las consultas eliminando espacios extra entre las palabras.
    assert any("INSERT INTO violations (carID, timestamp, fine)" in query for query in executed_queries), \
        "No se encontró la inserción esperada en violations"

    assert "RFID_123" in pending_violations, "El auto no fue agregado a pending_violations"

def test_process_pending_violations(mock_connection, mocker):
    """Verifica que después de 30 segundos la multa se mueva a violation_history y se envíe un correo"""
    mock_conn, mock_cursor = mock_connection
    pending_violations = {"RFID_123": datetime.now() - timedelta(seconds=35)}

    # Simular email del usuario
    mock_cursor.fetchone.return_value = ("juan@email.com",)

    # Simular el envío de correo
    mock_send_email = mocker.patch("violation_process_2.send_email")

    violation_process_2.process_pending_violations(mock_conn, pending_violations)

    # Verificar que se movió a violation_history
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert any("INSERT INTO violation_history (carID, timestamp, fine)" in query for query in executed_queries), \
        "No se encontró la inserción esperada en violation_history"

    # Verificar que el email fue enviado
    mock_send_email.assert_called_once()

    # Verificar que la multa fue eliminada de violations
    assert "RFID_123" not in pending_violations, "La multa no fue eliminada de pending_violations"

def test_rfid_lookup_performance(mock_connection):
    """Verifica que la consulta de RFID a la base de datos sea rápida"""
    import time
    mock_conn, mock_cursor = mock_connection
    mock_cursor.fetchone.side_effect = [
    (0,),  # Simula COUNT(*) en violation_history
    None,  # Simula que no hay multas en violations 
    ("Walker", "Engineering")  # Simula la consulta parking_in, building 
]


    start_time = time.time()
    violation_process_2.check_and_record_violation("RFID_123", "Juan", "juan@email.com", mock_conn, set(), {})
    end_time = time.time()

    assert end_time - start_time < 2, "La consulta de RFID tardó demasiado tiempo"

def test_sql_injection_protection(mock_connection):
    """Verifica que el sistema no sea vulnerable a SQL Injection"""
    mock_conn, mock_cursor = mock_connection

    # Simulamos un intento de SQL Injection
    bad_rfid = "'; DROP TABLE users; --"
    mock_cursor.fetchone.return_value = None  # No debería encontrar nada

    violation_process_2.check_and_record_violation(bad_rfid, "Hacker", "hacker@email.com", mock_conn, set(), {})

    # Asegurar que la consulta fue preparada correctamente
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert any("SELECT parking_in, building FROM users WHERE carID = %s" in query for query in executed_queries), \
        "Consulta SQL no protegida contra inyección"

def test_recent_violation(mock_connection, mocker):
    """Verifica que no se registre una multa si el usuario ya tiene una multa reciente en violation_history"""
    mock_conn, mock_cursor = mock_connection
    processed_users = set()
    pending_violations = {}

    # Simulamos que el usuario tiene una multa reciente
    mock_cursor.fetchone.side_effect = [
        (1,),  # El usuario tiene una multa reciente en violation_history
        None,  # No tiene multas activas en violations
        ("Walker", "Engineering")
    ]

    violation_process_2.check_and_record_violation(
        "RFID_123", "Juan", "juan@email.com", mock_conn, processed_users, pending_violations
    )

    # Verificar que no se haya registrado una nueva multa en violations
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert not any("INSERT INTO violations (carID, timestamp, fine)" in query for query in executed_queries), \
        "Se registró una multa aunque el usuario ya tiene una multa reciente"

def test_active_violation(mock_connection, mocker):
    """Verifica que no se registre una nueva multa si el usuario ya tiene una multa activa en violations"""
    mock_conn, mock_cursor = mock_connection
    processed_users = set()
    pending_violations = {}

    # Simulamos que el usuario tiene una multa activa
    mock_cursor.fetchone.side_effect = [
        (0,),  # No tiene multas recientes en violation_history
        ("2024-03-16 12:00:00",),  # Tiene una multa activa en violations
        ("Walker", "Engineering")
    ]

    violation_process_2.check_and_record_violation(
        "RFID_123", "Juan", "juan@email.com", mock_conn, processed_users, pending_violations
    )

    # Verificar que no se haya registrado una nueva multa en violations
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert not any("INSERT INTO violations (carID, timestamp, fine)" in query for query in executed_queries), \
        "Se registró una nueva multa aunque el usuario tiene una multa activa"

def test_correct_parking(mock_connection, mocker):
    """Verifica que no se registre una multa si el usuario está bien estacionado"""
    mock_conn, mock_cursor = mock_connection
    processed_users = set()
    pending_violations = {}

    # Simulamos que el usuario está bien estacionado
    mock_cursor.fetchone.side_effect = [
        (0,),  # No tiene multas recientes
        None,  # No tiene multas activas
        ("Walker", "Walker")  # Está estacionado correctamente
    ]

    violation_process_2.check_and_record_violation(
        "RFID_123", "Juan", "juan@email.com", mock_conn, processed_users, pending_violations
    )

    # Verificar que no se haya registrado una multa
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert not any("INSERT INTO violations (carID, timestamp, fine)" in query for query in executed_queries), \
        "Se registró una multa aunque el usuario está estacionado correctamente"

def test_process_violation_before_timeout(mock_connection):
    """Verifica que la multa no se mueva antes de 30 segundos"""
    mock_conn, mock_cursor = mock_connection
    pending_violations = {"RFID_123": datetime.now() - timedelta(seconds=10)}

    violation_process_2.process_pending_violations(mock_conn, pending_violations)

    # Verificar que no se movió a violation_history
    executed_queries = [" ".join(call[0][0].split()) for call in mock_cursor.execute.call_args_list]
    assert not any("INSERT INTO violation_history (carID, timestamp, fine)" in query for query in executed_queries), \
        "La multa se movió a violation_history antes de tiempo"
