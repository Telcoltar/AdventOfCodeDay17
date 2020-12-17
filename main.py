import logging
from itertools import product
from logging.config import fileConfig
from typing import TextIO

import numpy as np


def update_config(path):
    fileConfig(path)


def read_input_data(file_name: str) -> np.array:
    f: TextIO = open(file_name)

    grid: list[list[list[int]]] = [[]]
    current_line: list[int]

    for line in f.readlines():
        current_line = []
        for char in line.strip():
            if char == ".":
                current_line.append(0)
            else:
                current_line.append(1)
        grid[0].append(current_line)

    f.close()

    return np.array(grid)


def pad_grid(grid: np.array) -> np.array:
    return np.pad(grid, 1)


def get_active_neighbor_cubes(grid: np.array, origin: tuple[int, ...]) -> int:
    count: int = 0
    ranges: list[range] = [range(i - 1, i + 2) for i in origin]
    for indices in product(*ranges):
        if indices == origin:
            continue
        if grid[indices]:
            count += 1
    return count


def cycle_3d(grid: np.array) -> np.array:
    const_padded_grid: np.array = pad_grid(grid)
    padded_grid: np.array = pad_grid(grid)
    shape: tuple[int, int, int] = padded_grid.shape
    for indices in product(*[list(range(1, j - 1)) for j in shape]):
        if const_padded_grid[indices] == 1:
            logger.debug(f"coord: {indices}, AN: "
                         f"{get_active_neighbor_cubes(const_padded_grid, indices)}")
            if not 2 <= get_active_neighbor_cubes(const_padded_grid, indices) <= 3:
                padded_grid[indices] = 0
        else:
            if get_active_neighbor_cubes(const_padded_grid, indices) == 3:
                logger.debug(f"coord: {indices}, 1")
                padded_grid[indices] = 1
    return padded_grid


def solution_part_1(file_name: str) -> np.ndarray:
    grid: np.array = pad_grid(read_input_data(file_name))
    logger.debug(grid.shape)
    logger.debug(grid)
    for _ in range(6):
        grid = cycle_3d(grid)
    return np.sum(grid)


def cycle_4d(grid: np.array) -> np.array:
    const_padded_grid: np.array = pad_grid(grid)
    padded_grid: np.array = pad_grid(grid)
    shape: tuple[int, int, int, int] = padded_grid.shape
    logger.debug(shape)
    for indices in product(*[list(range(1, j - 1)) for j in shape]):
        if const_padded_grid[indices] == 1:
            logger.debug(f" coord: {indices}, AN: {get_active_neighbor_cubes(const_padded_grid, indices)}")
            if not 2 <= get_active_neighbor_cubes(const_padded_grid, indices) <= 3:
                padded_grid[indices] = 0
        else:
            if get_active_neighbor_cubes(const_padded_grid, indices) == 3:
                logger.debug(f"coord: {indices}, 1")
                padded_grid[indices] = 1
    return padded_grid


def solution_part_2(file_name: str) -> np.ndarray:
    grid: np.array = pad_grid(read_input_data(file_name)[np.newaxis, :])
    logger.debug(grid.shape)
    for _ in range(6):
        grid = cycle_4d(grid)
    return np.sum(grid)


if __name__ == '__main__':
    update_config("log.ini")
    logger = logging.getLogger('dev')
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
