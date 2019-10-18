from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import eventlet
import random
import os


class world():
    def __init__(self, rows, coloumns):
        self.rows = rows
        self.coloumns = coloumns
        self.map_positions = []
        self.characters = []

    def world_create(self):
        for coloumn in range(self.coloumns):
            self.map_positions.append([])
            for row in range(self.rows):
                self.map_positions[coloumn]
                spot = spots(coloumn, row)
                self.map_positions[coloumn].append(spot)

    def character_pos(self):
        for coloumn in self.map_positions:
            for position in coloumn:
                position.occupied = None
                for character in self.characters:
                    if position.x_cord == character.x and position.y_cord == character.y:
                        position.occupied = character.color

    def return_location(self, x=7, y=7):
        location = []
        position_count = 0
        check = 0
        for coloumn in range(x-2, x+3):
            for row in range(y-2, y+3):
                if coloumn < self.coloumns:
                    for position in self.map_positions[coloumn]:
                        if position.x_cord == coloumn and position.y_cord == row:
                            if position.occupied is not None:
                                location.append(position.occupied)
                                position_count += 1
                            else:
                                location.append(position.color)
                                position_count += 1
                check += 1
                if position_count < check:
                    position_count += 1
                    location.append('#000000')

        return location


class spots():
    def __init__(self, x, y):
        self.x_cord = x
        self.y_cord = y
        self.color_list = ['#FE1B04', '#FE9C04', '#F6FE04', '#01FD03', '#01FDB4', '#0174FD', '#C801FD']
        self.color = random.choice(self.color_list)
        self.occupied = None


class character():
    def __init__(self):
        self.id = str(random.random())
        self.x = 7
        self.y = 7
        self.color = '#030303'


new_world = world(20, 20)
new_world.world_create()
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    port = int(os.environ.get('PORT', 5000))
    return render_template('index.html', async_mode=socketio.async_mode, port=port)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('left', namespace='/test')
def left_key(message):
    global new_world
    session['receive_count'] = session.get('receive_count', 0) + 1
    current_character = session.get('character')
    current_character.x = current_character.x + 1
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)

        emit('veiw_port',
             {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('right', namespace='/test')
def right_key(message):
    global new_world
    session['receive_count'] = session.get('receive_count', 0) + 1
    current_character = session.get('character')
    current_character.x = current_character.x - 1
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)

        emit('veiw_port',
             {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('up', namespace='/test')
def up_key(message):
    global new_world
    session['receive_count'] = session.get('receive_count', 0) + 1
    current_character = session.get('character')
    current_character.y = current_character.y - 1
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)

        emit('veiw_port',
             {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('down', namespace='/test')
def down_key(message):
    global new_world
    session['receive_count'] = session.get('receive_count', 0) + 1
    current_character = session.get('character')
    current_character.y = current_character.y + 1
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)

        emit('veiw_port',
             {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    global new_world
    player = character()
    new_world.characters.append(player)
    session['character'] = player
    emit('connected', {'data': player.id, 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
