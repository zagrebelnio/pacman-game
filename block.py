
class Block:
    def __init__(self):
        self.__rect = []
    def reset(self, game_field):
        for y in range(game_field.getRows()):
            for x in range(game_field.getCols()):
                if game_field.getMatrix()[y][x] >= 3:
                    self.__rect.append([x * game_field.getGridSize(), y * game_field.getGridSize(), game_field.getGridSize(), game_field.getGridSize()])
    def check_wall_collisions(self, entity):
        # pacman-block collisions
        for block in self.__rect:
            # right collision
            if entity.getDirection() == "right" and block[0] - entity.getRadius() <= entity.getX() <= block[0] + block[
                2] - entity.getRadius() and block[1] <= entity.getY() <= block[1] + block[3]:
                entity.setX(block[0] - entity.getRadius())
            # left collision
            if entity.getDirection() == "left" and block[0] + entity.getRadius() <= entity.getX() <= block[0] + block[
                2] + entity.getRadius() and block[1] <= entity.getY() <= block[1] + block[3]:
                entity.setX(block[0] + block[2] + entity.getRadius())
            # top collision
            if entity.getDirection() == "up" and block[0] <= entity.getX() <= block[0] + block[2] and block[
                1] + entity.getRadius() <= entity.getY() <= block[1] + block[3] + entity.getRadius():
                entity.setY(block[1] + block[2] + entity.getRadius())
            # bottom collision
            if entity.getDirection() == "down" and block[0] <= entity.getX() <= block[0] + block[2] and block[
                1] - entity.getRadius() <= entity.getY() <= block[1] + block[3] - entity.getRadius():
                entity.setY(block[1] - entity.getRadius())