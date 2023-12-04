import re
from dataclasses import dataclass


@dataclass
class Cubes:
	red: int
	green: int
	blue: int


@dataclass
class Game:
	id: int
	cubes_sets: list[Cubes]
	is_valid: bool = True


MAX_CUBES_RED = 12
MAX_CUBES_GREEN = 13
MAX_CUBES_BLUE = 14


def parse_game(input_line: str) -> Game:
	"""
	Helper method for parsing a single game. This method extracts game id and cubes for each cubes sets.
	:param input_line: string representing single game
	:return: parsed game
	"""
	game_id = re.findall(r"Game (\d+):", input_line)
	game_id_parsed = int(game_id[0])
	prefix_len = 7 + len(game_id[0])
	line_trimmed = input_line[prefix_len:]
	cubes_sets = re.findall(r"([^;]+;?)", line_trimmed)
	cubes_parsed = []
	for cubes_set in cubes_sets:
		cubes = re.findall(r"(\d+) (\w+)", cubes_set)
		cubes_map = {color: count for count, color in cubes}
		cubes_parsed.append(Cubes(red=int(cubes_map.get('red', "0")),
								  green=int(cubes_map.get('green', "0")),
								  blue=int(cubes_map.get('blue', "0"))))
	return Game(id=game_id_parsed, cubes_sets=cubes_parsed)


def part_one(games: list[Game]) -> int:
	for game in games:
		if any([cubes_set.red > MAX_CUBES_RED or cubes_set.green > MAX_CUBES_GREEN or cubes_set.blue > MAX_CUBES_BLUE
				for cubes_set in game.cubes_sets]):
			game.is_valid = False
	return sum([game.id for game in games if game.is_valid])


def part_two(games: list[Game]) -> int:
	sum_of_maxes = 0
	for game in games:
		max_red = max([cubes_set.red for cubes_set in game.cubes_sets])
		max_green = max([cubes_set.green for cubes_set in game.cubes_sets])
		max_blue = max([cubes_set.blue for cubes_set in game.cubes_sets])
		sum_of_maxes += max_red * max_green * max_blue
	return sum_of_maxes


if __name__ == "__main__":
	with open("./input.txt", "r") as f:
		games = [parse_game(input_line=line) for line in f.readlines()]
	print(f"Part one: {part_one(games=games)}")
	print(f"Part two: {part_two(games=games)}")
