import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from main import app, get_db
from fastapi.testclient import TestClient
from database import SessionLocal
from sqlalchemy.orm import Session

load_dotenv()
engine = create_engine(os.getenv('TESTING_DATABASE_URL'))
TestingSessionLocal = SessionLocal


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_weather_data_without_filter():
    response = client.get('/api/weather/')
    assert response.status_code == 200
    assert response.json()['count'] == 10


def test_get_weather_data_with_station_id_as_filter():
    response = client.get('/api/weather/?station=USC00257715')
    assert response.status_code == 200
    assert response.json()['data'][0]['station'] == 'USC00257715'


def test_get_weather_data_with_date_as_filter():
    response = client.get('/api/weather/?date=1985-01-01')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '1985-01-01'


def test_get_weather_data_with_all_filters():
    response = client.get('/api/weather/?station=USC00110072&date=2010-03-02')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '2010-03-02'
    assert response.json()['data'][0]['station'] == 'USC00110072'


def test_get_weather_data_pagination():
    response = client.get('/api/weather/?page=1&limit=2')
    assert response.status_code == 200
    assert response.json()['count'] == 2


def test_get_weather_stats_with_no_filter():
    response = client.get('/api/weather/stats/')
    assert response.status_code == 200
    assert response.json()['count'] == 10


def test_get_stats_data_with_station_id_as_filter():
    response = client.get('/api/weather/stats?station=USC00331592')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['station'] == 'USC00331592'


def test_all_records_data_with_year_as_filter():
    response = client.get('/api/weather/stats/?year=1999')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['year'] == 1999


def test_all_records_data_with_all_filters():
    response = client.get('/api/weather/stats/?year=2006&station=USC00336118')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['data'][0]['year'] == 2006
    assert response.json()['data'][0]['station'] == 'USC00336118'


def test_all_records_data_pagination():
    response = client.get('/api/weather/stats/?page=0&limit=3')
    assert response.json()['count'] == 3


def test_all_records_data_invalid_weather():
    response1 = client.get('api/weather/?station=fgfsdf')
    response2 = client.get('api/weather/?date=2024-01-01')
    assert response1.status_code == 400
    assert response2.status_code == 400


def test_stats_records_invalid_filters():
    response1 = client.get('api/weather/stats?station=fgfsdg')
    response2 = client.get('api/weather/stats?year=2024')
    assert response1.status_code == 400
    assert response2.status_code == 400



