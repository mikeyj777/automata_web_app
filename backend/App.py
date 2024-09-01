# backend/app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from simulation.engine import SimulationEngine
import threading
import eventlet

eventlet.monkey_patch()  # Necessary for Flask-SocketIO with eventlet

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Initialize Simulation Engine
engine = SimulationEngine(bounds=(100, 100))
engine.initialize_agents(num_agents=50)

def simulation_thread():
    while engine.running:
        engine.update()
        state = engine.get_state()
        socketio.emit('update', state)
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
    socketio.run(app, host='0.0.0.0', port=5000)
