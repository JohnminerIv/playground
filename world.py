import random


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

    def return_location(self, x=0, y=0):
        location = []
        position_count = 0
        check = 0
        for coloumn in range(x-2, x+3):
            for row in range(y-2, y+3):
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
print(new_world.return_location())
