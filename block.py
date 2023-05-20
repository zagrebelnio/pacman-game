
class Block:
    def __init__(self):
        self.rect = []
    def reset(self, game_field):
        for y in range(game_field.rows):
            for x in range(game_field.cols):
                if game_field.matrix[y][x] == 1:
                    self.rect.append([x * game_field.grid_size, y * game_field.grid_size, game_field.grid_size, game_field.grid_size])
    def check_wall_collisions(self, pacman):
        # pacman-block collisions
        for block in self.rect:
            # right collision
            if pacman.direction == "right" and block[0] - pacman.radius <= pacman.x <= block[0] + block[
                2] - pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
                pacman.x = block[0] - pacman.radius
            # left collision
            if pacman.direction == "left" and block[0] + pacman.radius <= pacman.x <= block[0] + block[
                2] + pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
                pacman.x = block[0] + block[2] + pacman.radius
            # top collision
            if pacman.direction == "up" and block[0] <= pacman.x <= block[0] + block[2] and block[
                1] + pacman.radius <= pacman.y <= block[1] + block[3] + pacman.radius:
                pacman.y = block[1] + block[2] + pacman.radius
            # bottom collision
            if pacman.direction == "down" and block[0] <= pacman.x <= block[0] + block[2] and block[
                1] - pacman.radius <= pacman.y <= block[1] + block[3] - pacman.radius:
                pacman.y = block[1] - pacman.radius