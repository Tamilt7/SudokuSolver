from flask import Flask, request, jsonify

app = Flask(__name__)
cache = {}


@app.route('/set', methods=['POST'])
def set_cache():
    data = request.json
    cache[data['key']] = data['value']
    return jsonify({"status": "success"}), 200


@app.route('/get/<key>', methods=['GET'])
def get_cache(key):
    value = cache.get(key, None)
    return jsonify({"value": value}), 200


if __name__ == "__main__":
    app.run(port=5000)


import requests

def main_process():
    print("Main process started...")
    # Set a value in the cache
    requests.post("http://127.0.0.1:5000/set", json={"key": "example_key", "value": "example_value"})
    # Get a value from the cache
    response = requests.get("http://127.0.0.1:5000/get/example_key")
    print("Cache Response:", response.json())

if __name__ == "__main__":
    main_process()