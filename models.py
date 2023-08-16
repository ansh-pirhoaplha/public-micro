from pydantic import BaseModel

class SensorLog(BaseModel):
    timestamp: str
    unique_id: str
    sensor_id: int
    value: float


# Example data
log_data = {
    "timestamp": "2023-08-08 12:00:00",
    "unique_id": "3R6HuuiV",
    "sensor_id": 1,
    "value": 25.5
}

# Validate and create a SensorLog instance
sensor_log = SensorLog(**log_data)