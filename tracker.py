from flask import Flask, request, jsonify
app = Flask(__name__)

# This dictionary will hold the file information.
# Key: File ID, Value: List of tuples (peer_address, chunk_name)
file_registry = {}

@app.route('/register', methods=['POST'])
def register_chunk():
    """
    Register a file chunk with the tracker.
    Expects JSON in the form: {'file_id': 'file123', 'peer_address': '192.168.1.5', 'chunk_name': 'chunk001.bin'}
    """
    data = request.json
    file_id = data['file_id']
    peer_address = data['peer_address']
    chunk_name = data['chunk_name']

    if file_id not in file_registry:
        file_registry[file_id] = []
    file_registry[file_id].append((peer_address, chunk_name))

    return jsonify({'message': 'Chunk registered successfully'}), 200

@app.route('/get_peers', methods=['GET'])
def get_peers():
    """
    Get a list of peers for a specific file.
    Expects a file ID as query parameter.
    """
    file_id = request.args.get('file_id')
    if file_id in file_registry:
        return jsonify(file_registry[file_id])
    else:
        return jsonify({'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
