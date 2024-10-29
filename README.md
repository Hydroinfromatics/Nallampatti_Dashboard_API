# Nallampatti_Dashboard_API
# Sensor Data API

A Flask-based REST API for collecting, storing, and serving real-time and historical sensor data. This application fetches data from sensors, processes it, and provides multiple endpoints to access both current and historical data.

## Features

- Real-time sensor data collection
- Historical data storage and retrieval
- Customizable date range queries
- Pre-defined time range queries (7 days, 30 days)
- RESTful API endpoints
- Automatic data processing
- Error handling and validation

## Tech Stack

- Python 3.x
- Flask (Web Framework)
- Pandas (Data Processing)
- Gunicorn (WSGI HTTP Server)
- Render (Deployment Platform)

## API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | API documentation | None |
| `/health` | GET | Health check endpoint | None |
| `/update_data` | GET | Trigger sensor data update | None |
| `/sensor_data` | GET | Get today's sensor data | None |
| `/historical_data` | GET | Get data for date range | `start_date`, `end_date` (YYYY-MM-DD) |
| `/data_by_date/<date>` | GET | Get data for specific date | `date` (YYYY-MM-DD) |
| `/data_range/last_7_days` | GET | Get last 7 days data | None |
| `/data_range/last_30_days` | GET | Get last 30 days data | None |

## Example API Calls

1. **Get Today's Data**
```http
GET /sensor_data
```

2. **Get Historical Data**
```http
GET /historical_data?start_date=2024-10-01&end_date=2024-10-29
```

3. **Get Specific Date Data**
```http
GET /data_by_date/2024-10-29
```

4. **Get Last 7 Days Data**
```http
GET /data_range/last_7_days
```

## Response Format

```json
{
    "status": "success",
    "count": 24,
    "data": [
        {
            "timestamp": "2024-10-29T10:00:00",
            "pH": 7.2,
            "TDS": 450,
            "Depth": 12.5,
            "FlowInd": 25.3
        }
    ]
}
```

## Local Setup

1. **Clone the repository**
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
# On Unix/macOS:
export API_URL='your-sensor-api-url'

# On Windows:
set API_URL=your-sensor-api-url
```

5. **Run the application**
```bash
python app.py
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add environment variables:
   - `API_URL`: Your sensor API endpoint

## Project Structure
```
project/
├── app.py               # Main Flask application
├── data_process.py      # Data processing logic
├── get_data.py         # API fetch logic
├── requirements.txt     # Project dependencies
└── README.md           # Documentation
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| API_URL | Sensor API endpoint URL | Yes |
| PORT | Application port (default: 5000) | No |

## Error Handling

The API returns standard HTTP status codes:
- 200: Successful request
- 400: Bad request (invalid parameters)
- 404: Endpoint not found
- 500: Internal server error

Example error response:
```json
{
    "status": "error",
    "message": "Invalid date format. Use YYYY-MM-DD"
}
```

## Data Validation

- Dates must be in YYYY-MM-DD format
- Date ranges must be valid (start_date ≤ end_date)
- All timestamps are returned in ISO format

## Monitoring

- Use the `/health` endpoint for uptime monitoring
- Check logs in Render dashboard
- Monitor data updates through the update_data endpoint

## Limitations

- Data retention period based on available storage
- Rate limiting on Render's free tier
- Maximum request payload size

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please:
1. Check existing documentation
2. Review error messages
3. Check Render logs
4. Create an issue in the repository


## Contact

[Gurudev]
