from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

# ── Database connection ───────────────────────────────────────
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="processordb",
        user="postgres",
        password="aditya2007",
        port="5432"
    )

# ── Serve HTML + static files ─────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/ranks.html')
def ranks():
    return send_from_directory(BASE_DIR, 'ranks.html')

@app.route('/compare.html')
def compare():
    return send_from_directory(BASE_DIR, 'compare.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

# ── API: All processors ───────────────────────────────────────
@app.route('/api/processors', methods=['GET'])
def get_processors():
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM processors ORDER BY nanoscore DESC")
        rows      = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()

        result = []
        for row in rows:
            proc      = dict(zip(col_names, row))
            pros_raw  = proc.get('pros', '') or ''
            pros_list = [p.strip() for p in pros_raw.split(',') if p.strip()]

            result.append({
                "id":        proc.get('id'),
                "name":      proc.get('name'),
                "company":   proc.get('company'),
                "cpu":       proc.get('cpu'),
                "gpu":       proc.get('gpu'),
                "battery":   proc.get('battery'),
                "nanoscore": proc.get('nanoscore'),
                "antutu":    proc.get('antutu', 0)      or 0,
                "process":   proc.get('process', 'N/A') or 'N/A',
                "pros":      pros_list
            })

        print(f"✅ /api/processors → {len(result)} rows")
        return jsonify(result)

    except Exception as e:
        print(f"❌ DB ERROR: {e}")
        return jsonify({"error": str(e)}), 500

# ── Run ───────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f"📂 Serving files from: {BASE_DIR}")
    print(f"🚀 Open http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
