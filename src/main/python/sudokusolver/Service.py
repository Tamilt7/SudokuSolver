import threading
import socketio
import requests
from datetime import datetime

pulsar_url = "http://127.0.0.1:5000/set"


class Service:
    def __init__(self, backend_url=pulsar_url):
        self.backend_url = backend_url
        self.stt_time = datetime.now()

        self.waiting_for_response = False
        self.session_id = None
        self.response_data = None

        self.sio = socketio.Client()

        # Attach event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('solution_found', self.on_solution_received)
        self.sio.on('session_id', self.get_session_id)

        # Start the socket connection in a separate thread
        threading.Thread(target=self.connect_socketio, daemon=True).start()

    def connect_socketio(self):
        """Connect to the SocketIO server in a background thread."""
        self.sio.connect(self.backend_url)

    @staticmethod
    def on_connect():
        print("Connected to Pulsar via WebSocket!")

    def get_session_id(self, data):
        print('Session ID received:', data['session_id'])
        self.session_id = data['session_id']

    def on_solution_received(self, payload):
        if payload['solution']:
            self.response_data = payload['solution']
            print(f"Pulsar took {payload['duration']} seconds to solve the puzzle")
            print(f"Total time: {datetime.now() - self.stt_time}")
        else:
            print(f"Pulsar took {payload['duration']} seconds and could not find a solution :(")

        self.waiting_for_response = False

    def on_disconnect(self):
        self.waiting_for_response = False
        print("Disconnected from Pulsar.")

    def send_pulsar_request(self, puzzle, solver='sequential'):
        if self.waiting_for_response:
            print("Please wait until your previous request is resolved!")
            return

        if self.response_data:
            print("Please clear the previous response and try again!")
            return

        self.stt_time = datetime.now()
        try:
            payload = {"action": "solve_puzzle",
                       "puzzle": puzzle.question,
                       "solver": solver,
                       "session_id": self.session_id}

            response = requests.post(pulsar_url, json=payload, timeout=1)
            if response.status_code == 200:
                print("")
                print("Request sent to Pulsar!")
                self.waiting_for_response = True
            else:
                print(f"Failed to send puzzle: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while sending puzzle: {e}")
