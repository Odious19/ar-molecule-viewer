from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "AR Molecule Server is running!"})

@app.route('/fetch-pdb/<pdb_id>')
def fetch_pdb(pdb_id):
    """Fetch PDB file from RCSB and convert to GLB"""
    try:
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        response = requests.get(url)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "pdb_id": pdb_id,
                "data": response.text
            })
        else:
            return jsonify({"error": "PDB not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
