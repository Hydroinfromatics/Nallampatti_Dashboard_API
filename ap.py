from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from datetime import datetime, timedelta
from data_process import process_and_store_data, get_todays_data, get_historical_data
import os

app = Flask(__name__)
CORS(app)

# Configuration
API_URL = os.environ.get('API_URL', 'default_api_url')

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Sensor Data API is active",
        "endpoints": [
            "/health",
            "/update_data",
            "/sensor_data",
            "/historical_data?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD",
            "/data_by_date/YYYY-MM-DD",
            "/data_range/last_7_days",
            "/data_range/last_30_days"
        ]
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/update_data')
def update_data():
    try:
        process_and_store_data(API_URL)
        return jsonify({
            "status": "success",
            "message": "Data updated successfully",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/sensor_data')
def get_sensor_data():
    try:
        data = get_todays_data()
        if data.empty:
            return jsonify({
                "status": "success",
                "message": "No data available for today",
                "data": []
            })
        
        # Clean NaN values
        data.fillna(value=None, inplace=True)  # or use another default value if needed
        json_data = data.to_json(orient='records', date_format='iso')  # Convert to JSON
        
        # Ensure json_data is a valid JSON object
        return jsonify({
            "status": "success",
            "count": len(data),
            "data": json.loads(json_data)  # Ensure it's a proper JSON object
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/historical_data')
def get_historical_data_range():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({
                "status": "error",
                "message": "Both start_date and end_date are required (format: YYYY-MM-DD)"
            }), 400
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        data = get_historical_data(start_date, end_date)
        if data.empty:
            return jsonify({
                "status": "success",
                "message": "No data available for the specified date range",
                "data": []
            })

        # Clean NaN values
        data.fillna(value=None, inplace=True)
        json_data = data.to_dict(orient='records')
        return jsonify({
            "status": "success",
            "count": len(json_data),
            "date_range": {
                "start": start_date.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d')
            },
            "data": json_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/data_by_date/<date>')
def get_data_by_date(date):
    try:
        try:
            query_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        data = get_historical_data(query_date, query_date)
        if data.empty:
            return jsonify({
                "status": "success",
                "message": f"No data available for {date}",
                "data": []
            })

        # Clean NaN values
        data.fillna(value=None, inplace=True)
        json_data = data.to_dict(orient='records')
        return jsonify({
            "status": "success",
            "date": date,
            "count": len(json_data),
            "data": json_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/data_range/<range_type>')
def get_data_range(range_type):
    try:
        end_date = datetime.now()
        
        if range_type == 'last_7_days':
            start_date = end_date - timedelta(days=7)
        elif range_type == 'last_30_days':
            start_date = end_date - timedelta(days=30)
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid range_type. Use 'last_7_days' or 'last_30_days'"
            }), 400

        data = get_historical_data(start_date, end_date)
        if data.empty:
            return jsonify({
                "status": "success",
                "message": "No data available for the specified range",
                "data": []
            })

        # Clean NaN values
        data.fillna(value=None, inplace=True)
        json_data = data.to_dict(orient='records')
        return jsonify({
            "status": "success",
            "range_type": range_type,
            "count": len(json_data),
            "date_range": {
                "start": start_date.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d')
            },
            "data": json_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
