from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import random
import os
from dotenv import load_dotenv
load_dotenv()

in_production = os.getenv("INPRODUCTION")
port = os.getenv("PORT")

class world():
    def __init__(self, rows, coloumns):
        self.rows = rows
        self.coloumns = coloumns
        self.map_positions = []
        self.characters = []

    def world_create(self):
        '''Creates postitions for each point on the map.'''
        for coloumn in range(self.coloumns):
            self.map_positions.append([])
            for row in range(self.rows):
                self.map_positions[coloumn]
                spot = spots(coloumn, row)
                self.map_positions[coloumn].append(spot)

    def character_pos(self):
        '''Updates where each of the players are at.'''
        for coloumn in self.map_positions:
            for position in coloumn:
                position.occupied = None
                for character in self.characters:
                    if position.x_cord == character.x and position.y_cord == character.y:
                        position.occupied = character.color


    def return_location(self, x=7, y=7):
        '''Returns what each play can see.'''
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
        """Builds a spot on the map."""
        self.x_cord = x
        self.y_cord = y
        self.color_list = ['#FE1B04', '#FE9C04', '#F6FE04', '#01FD03', '#01FDB4', '#0174FD', '#C801FD']
        self.color = random.choice(self.color_list)
        self.occupied = None


class character():
    def __init__(self):
        '''Creates a player with random starting position.'''
        self.id = str(random.random())
        self.x = random.randint(0, new_world.coloumns - 1)
        self.y = random.randint(0, new_world.rows - 1)
        self.color = '#030303'

    def right(self):
        new_world.character_pos()
        if new_world.map_positions[self.x - 1][self.y].occupied is None:
            self.x = self.x - 1

    def left(self):
        new_world.character_pos()
        if new_world.map_positions[self.x + 1][self.y].occupied is None:
            self.x = self.x + 1

    def up(self):
        new_world.character_pos()
        if new_world.map_positions[self.x][self.y - 1].occupied is None:
            self.y = self.y - 1

    def down(self):
        new_world.character_pos()
        if new_world.map_positions[self.x][self.y + 1].occupied is None:
            self.y = self.y + 1


new_world = world(20, 20)
new_world.world_create()
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    if in_production == "true":
        port = 80
    else:
        port = os.getenv("PORT")
    return render_template('index.html', async_mode=socketio.async_mode, port=port)


@socketio.on('left', namespace='/test')
def left_key(message):
    global new_world
    current_character = session.get('character')
    if current_character.x + 1 < new_world.coloumns:
        current_character.left()
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('right', namespace='/test')
def right_key(message):
    global new_world
    current_character = session.get('character')
    if current_character.x - 1 > -1:
        current_character.right()
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('up', namespace='/test')
def up_key(message):
    global new_world
    current_character = session.get('character')
    if current_character.y - 1 > -1:
        current_character.up()
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('down', namespace='/test')
def down_key(message):
    global new_world
    current_character = session.get('character')
    if current_character.y + 1 < new_world.rows:
        current_character.down()
    session['character'] = current_character
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    global new_world
    player = character()
    new_world.characters.append(player)
    session['character'] = player
    emit('connected', {'data': player.id, 'count': 0})
    new_world.character_pos()
    for _character in new_world.characters:
        char_id = _character.id
        veiw = new_world.return_location(_character.x, _character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    player = session.get('character')
    new_world.characters.remove(player)
    new_world.character_pos()
    for character in new_world.characters:
        char_id = character.id
        veiw = new_world.return_location(character.x, character.y)
        emit('veiw_port', {'data': char_id, 'veiw': veiw}, broadcast=True)
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    if in_production == "true":
        socketio.run(app, host="0.0.0.0", debug=False, port=port)
    else:
        socketio.run(app, debug=True, port=port)
