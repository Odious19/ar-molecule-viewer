from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is Live. Fetching from PDB Database."

@app.route("/get-molecule")
def get_molecule():
    pdb_id = request.args.get("name", "").strip().upper()
    if not pdb_id:
        return jsonify({"error": "Missing PDB ID"}), 400

    # Fetch from RCSB PDB Database
    pdb_url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
    
    try:
        response = requests.get(pdb_url, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": f"PDB {pdb_id} not found"}), 404

        atoms = []
        # Parse PDB format
        for line in response.text.splitlines():
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # Extract coordinates and element
                element = line[76:78].strip()
                if not element: element = line[12:16].strip()[0]
                
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    
                    # Scale down by 10 so it fits in AR view
                    atoms.append({
                        "element": element,
                        "x": x / 10.0,
                        "y": y / 10.0,
                        "z": z / 10.0
                    })
                except: continue

        # Limit to 1000 atoms to prevent crashing the browser for huge proteins
        return jsonify({"pdb_id": pdb_id, "atoms": atoms[:1000]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
