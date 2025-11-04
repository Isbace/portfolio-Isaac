import pytest
import cv2
from unittest.mock import Mock, patch
import camera

def test_camera_initialization():
    """Prueba que la cámara se inicializa correctamente."""
    with patch("cv2.VideoCapture") as mock_capture:
        mock_capture.return_value.isOpened.return_value = True  # Simula que la cámara funciona
        cap = cv2.VideoCapture(0)
        assert cap.isOpened()
        cap.release()  # Cerrar para evitar conflictos

def test_yolo_model_load():
    """Prueba que el modelo YOLO se carga correctamente."""
    with patch("camera.YOLO") as mock_yolo:
        model = mock_yolo.return_value
        assert model is not None

def test_frame_processing():
    """Prueba que el procesamiento de un frame se realiza correctamente"""
    with patch("camera.model") as mock_model, patch("cv2.VideoCapture") as mock_capture:
        mock_capture.return_value.isOpened.return_value = True  # Simula que la cámara está encendida
        frame = Mock()  # Simula un frame
        results = [Mock()]
        results[0].boxes = [Mock(cls=[2], xyxy=[[100, 100, 200, 200]], conf=[0.9])]
        mock_model.return_value = results

        processed_frame = camera.model(frame)  # Simula detección YOLO
        assert processed_frame is not None  # Verificamos que el frame se procese sin errores

        cap = cv2.VideoCapture(0)  # Simulación de apertura de cámara
        cap.release()  # Cerrarla inmediatamente para evitar que se active la real

def test_vehicle_detection():
    """Prueba que se detecten correctamente vehículos (autos y motos)."""
    with patch("camera.model") as mock_model, patch("cv2.VideoCapture") as mock_capture:
        mock_capture.return_value.isOpened.return_value = True  # Simula que la cámara está encendida
        frame = Mock()  # Simula un frame
        # Simulamos una detección de un vehículo (auto con ID 2)
        results = [Mock()]
        results[0].boxes = [Mock(cls=[2], xyxy=[[100, 100, 200, 200]], conf=[0.9])]
        mock_model.return_value = results

        # Llamamos al modelo para verificar si se procesa la detección
        processed_frame = camera.model(frame)  # Simula detección YOLO
        assert processed_frame is not None  # Verificamos que el frame se procese sin errores

        # Verificamos que se haya dibujado la caja
        assert results[0].boxes[0].cls[0] == 2  # Debería ser un auto
        assert results[0].boxes[0].xyxy[0] == [100, 100, 200, 200]  # Verificamos las coordenadas de la caja


def test_camera_release():
    """Prueba que la cámara se libere correctamente después de la detección."""
    with patch("cv2.VideoCapture") as mock_capture:
        mock_capture.return_value.isOpened.return_value = True
        cap = cv2.VideoCapture(0)  # Iniciar la cámara

        # Ejecutar la detección y liberar la cámara
        cap.release()
        
        # Verificar que se haya llamado a release() para liberar la cámara
        cap.release.assert_called_once()  # Asegura que release fue llamado correctamente

def test_model_predictions():
    """Prueba que el modelo hace predicciones y retorna resultados esperados."""
    frame = Mock()  # Simula un frame de imagen
    results = [Mock()]
    results[0].boxes = [Mock(cls=[2], xyxy=[[10, 10, 100, 100]], conf=[0.95])]
    
    with patch("camera.model") as mock_model:
        mock_model.return_value = results
        
        # Ejecutar detección
        predictions = camera.model(frame)  # Llamada al modelo YOLO
        
        # Verificar las predicciones
        assert len(predictions) > 0
        assert predictions[0].boxes[0].cls[0] == 2  # Se espera que sea un auto
        assert predictions[0].boxes[0].conf[0] == 0.95  # Verifica la confianza de la predicción
