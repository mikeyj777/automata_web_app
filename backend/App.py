# backend/app.py

import eventlet
eventlet.monkey_patch()  # Necessary for Flask-SocketIO with eventlet

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from simulation.engine import SimulationEngine
import threading
from config import Config

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
CORS(app, origins=['127.0.0.1'])  # Allow specific origin
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins=['127.0.0.1'], async_mode='eventlet',log_level='debug')

# Initialize Simulation Engine
engine = SimulationEngine(bounds=(300, 300))
engine.initialize_agents(num_agents=1)

def simulation_thread():
    logging.info('Simulation thread started')
    while engine.running:

        engine.update()
        state = engine.get_state()
        # logging.debug(f'State retrieved\n\n\n')
        # Ensure state contains 'agents' and it's an array
        if isinstance(state, list):
            # logging.debug(f'Emitting state: {state}')
            socketio.emit('update', state)
        else:
            logging.warning(f'State is not a list: {state}')
            break
        socketio.sleep(0.1)  # Sleep for 100ms

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return "Agent-Based Model Backend"

if __name__ == '__main__':
    engine.running = True
    socketio.start_background_task(simulation_thread)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # restricts connections to only coming from my machine
