from Entities import GridCell
from Data import get_animal_picture_url


def generate_grid_cell(animals, grid_size):
    grid = []
    grid_line = []
    animal_flag = False
    for y in range(grid_size):
        for x in range(grid_size):
            for animal in animals:
                if animal.x == x and animal.y == y:
                    grid_line.append(GridCell([x, y, get_animal_picture_url(animal.pet_type.description), animal.pet_type]))
                    animal_flag = True
            if not animal_flag:
                grid_line.append(GridCell([x, y, get_animal_picture_url("none"), None]))
            animal_flag = False
        grid.append(grid_line)
        grid_line = []
    return grid
