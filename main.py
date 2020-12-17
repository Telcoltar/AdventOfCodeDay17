import logging
from argparse import ArgumentParser
from typing import TextIO
from itertools import product

import numpy as np

parser: ArgumentParser = ArgumentParser()

parser.add_argument("--log", default="info")

options = parser.parse_args()

level = logging.DEBUG

if options.log.lower() == "info":
    level = logging.INFO

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    level=level)

logger = logging.getLogger(__name__)


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


def get_active_neighbor_cubes_3d(grid: np.array, x: int, y: int, z: int) -> int:
    count: int = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            for k in range(z - 1, z + 2):
                if i == x and j == y and k == z:
                    continue
                if grid[k, j, i]:
                    count += 1
    # logger.debug(f"x: {x}, y: {y}, z: {z}, count: {count}")
    return count


def cycle_3d(grid: np.array) -> np.array:
    const_padded_grid: np.array = pad_grid(grid)
    padded_grid: np.array = pad_grid(grid)
    shape: tuple[int, int, int] = padded_grid.shape
    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            for k in range(1, shape[2] - 1):
                if const_padded_grid[i, j, k] == 1:
                    logger.debug(f"x: {k}, y: {j}, z: {i}, AN: "
                                 f"{get_active_neighbor_cubes_3d(const_padded_grid, k, j, i)}")
                    if not 2 <= get_active_neighbor_cubes_3d(const_padded_grid, k, j, i) <= 3:
                        padded_grid[i, j, k] = 0
                else:
                    if get_active_neighbor_cubes_3d(const_padded_grid, k, j, i) == 3:
                        logger.debug(f"x: {k}, y: {j}, z: {i}, 1")
                        padded_grid[i, j, k] = 1
    return padded_grid


def solution_part_1(file_name: str) -> np.ndarray:
    grid: np.array = pad_grid(read_input_data(file_name))
    logger.debug(grid.shape)
    logger.debug(grid)
    for _ in range(6):
        grid = cycle_3d(grid)
    return np.sum(grid)


def get_active_neighbor_cubes_4d(grid: np.array, origin: tuple[int, int, int, int]) -> int:
    count: int = 0
    ranges: list[range] = [range(i-1, i+2) for i in origin]
    for indices in product(*ranges):
        if indices == origin:
            continue
        if grid[indices]:
            count += 1
    # logger.debug(f"x: {x}, y: {y}, z: {z}, count: {count}")
    return count


def cycle_4d(grid: np.array) -> np.array:
    const_padded_grid: np.array = pad_grid(grid)
    padded_grid: np.array = pad_grid(grid)
    shape: tuple[int, int, int, int] = padded_grid.shape
    logger.debug(shape)
    for indices in product(*[list(range(1, j-1)) for j in shape]):
        if const_padded_grid[indices] == 1:
            logger.debug(f" coord: {indices}, AN: {get_active_neighbor_cubes_4d(const_padded_grid, indices)}")
            if not 2 <= get_active_neighbor_cubes_4d(const_padded_grid, indices) <= 3:
                padded_grid[indices] = 0
        else:
            if get_active_neighbor_cubes_4d(const_padded_grid, indices) == 3:
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
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
