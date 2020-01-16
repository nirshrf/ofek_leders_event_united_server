def generate_cell_animals_history(x, y, total_samples, heat_map):
    """
    x, y - coordinates of the rectangle to generate history for
    total_samples - total_number of sample history for the rectangle
    heat_map - heat_map to generate history according to
    """
    animals_history = {}
    for animal in heat_map[x][y]:
        animals_history[animal] = int(total_samples*heat_map[x][y][animal])
    return animals_history
