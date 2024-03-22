from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
