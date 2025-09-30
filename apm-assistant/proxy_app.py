import os, requests, time
from flask import Flask, jsonify, Response, request, stream_with_context
app = Flask(__name__)

TARGET_PORT = int(os.environ.get('BRIDGE_PORT', '8081'))
TARGET_HOST = '127.0.0.1'
TARGET_BASE = f'http://{TARGET_HOST}:{TARGET_PORT}'

def is_target_alive():
    try:
        r = requests.get(f'{TARGET_BASE}/', timeout=1)
        return r.status_code < 500
    except Exception:
        return False

@app.route('/apm-assistant/api/auto-fill', methods=['GET'])
def autofill():
    # Try proxying to target app
    if is_target_alive():
        try:
            r = requests.get(f'{TARGET_BASE}/apm-assistant/api/auto-fill', timeout=5)
            return Response(r.content, status=r.status_code, content_type=r.headers.get('Content-Type','application/json'))
        except Exception as e:
            # fall through to mock
            pass
    # Fallback mock response
    sample = {
        "form_id":"APM-2025-0001",
        "location":"FC-ATL-01",
        "asset":"Conveyor-7B",
        "reported_by":"Ethan W.",
        "date":"2025-09-30",
        "fields":{
            "symptom":"Intermittent belt slip during starting",
            "severity":"Medium",
            "last_maintenance":"2025-08-12",
            "suggested_action":"Inspect tensioner, replace worn idler roller",
            "estimated_downtime":"1 hour"
        },
        "confidence":0.92,
        "notes":"Auto-filled by EverLightOS APM Assistant (proxy fallback)"
    }
    return jsonify(sample)

# generic proxy route forwards any path under /apm-assistant to the target
@app.route('/apm-assistant/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def proxy_any(path):
    if is_target_alive():
        try:
            url = f'{TARGET_BASE}/apm-assistant/{path}'
            headers = {k:v for k,v in request.headers if k.lower() != 'host'}
            resp = requests.request(request.method, url, headers=headers, data=request.get_data(), params=request.args, stream=True, timeout=10)
            return Response(stream_with_context(resp.iter_content(chunk_size=8192)), status=resp.status_code, headers=resp.headers)
        except Exception as e:
            return jsonify({"error":"proxy failed","reason":str(e)}), 502
    return jsonify({"error":"target-unavailable","message":"BridgeOps app not running; proxy falling back to mock."}), 503

if __name__ == '__main__':
    # wait a few seconds for target to come up
    time.sleep(1)
    app.run(host='0.0.0.0', port=8080)
