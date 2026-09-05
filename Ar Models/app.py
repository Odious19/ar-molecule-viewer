from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "AR Molecule Viewer backend is running."


@app.route("/get-molecule")
def get_molecule():
    pdb_id = request.args.get("name", "").strip().upper()

    if not pdb_id:
        return jsonify({"error": "Missing PDB ID"}), 400

    pdb_url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    try:
        response = requests.get(pdb_url, timeout=15)

        if response.status_code != 200:
            return jsonify({"error": f"PDB {pdb_id} not found"}), 404

        pdb_text = response.text
        atoms = []

        for line in pdb_text.splitlines():
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    element = line[76:78].strip()
                    if not element:
                        element = line[12:16].strip()[0]

                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())

                    atoms.append({
                        "element": element,
                        "x": x / 10.0,
                        "y": y / 10.0,
                        "z": z / 10.0
                    })
                except:
                    continue

        if not atoms:
            return jsonify({"error": f"No atoms found in PDB {pdb_id}"}), 404

        return jsonify({
            "pdb_id": pdb_id,
            "atoms": atoms
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
