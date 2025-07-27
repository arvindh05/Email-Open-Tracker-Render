# Test 6

from flask import Flask, request, send_file, jsonify, Response
from datetime import datetime, timezone
import os
import csv
import requests

app = Flask(__name__)

# Paths
CSV_FILE = '/tmp/open_logs.csv'  # Temp directory (persists while app is running)

CSV_HEADERS = ['email_id', 'timestamp', 'ip', 'location', 'user_agent']

# In-memory logs (for JSON API)
open_logs = []

# Init CSV file with header
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)

# Save log to both CSV and memory
def log_open(email_id, ip, ua, location):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    row = [email_id, timestamp, ip, location, ua]
    open_logs.append(row)

    # Append to CSV file
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"[OPEN] Email ID: {email_id} | IP: {ip} | Location: {location} | UA: {ua}")

# GeoIP lookup
def get_location(ip):
    try:
        if ip.startswith("127.") or ip.startswith("::1"):
            return "Localhost"
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        data = resp.json()
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        return ", ".join(filter(None, [city, region, country]))
    except:
        return "Unknown"

# Tracking pixel route
@app.route('/track/<email_id>.png')
def track_open(email_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    location = get_location(ip)

    log_open(email_id, ip, ua, location)

    return send_file('transparent.png', mimetype='image/png')

@app.route('/view_logs/<email_id>')
def view_logs(email_id):
    results = []
    for row in open_logs:
        if row[0] == email_id:  # row[0] is email_id
            results.append(dict(zip(CSV_HEADERS, row)))  # Convert to dict for JSON

    return jsonify({
        "email_id": email_id,
        "open_count": len(results),
        "events": results
    })


# Download all logs as CSV
@app.route('/download_logs')
def download_logs():
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "No logs available"}), 404

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        csv_content = f.read()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=open_logs.csv"}
    )

if __name__ == '__main__':
    init_csv()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
