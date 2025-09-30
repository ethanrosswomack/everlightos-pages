from flask import Flask, jsonify, request
app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/auto-fill")
def autofill():
    # same payload as your page's fallback, so the demo matches
    return jsonify({
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
        "confidence":0.87,
        "notes":"Auto-filled by EverLightOS APM Assistant (mock)"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
