from collections import defaultdict
from dataclasses import dataclass
from functools import reduce


@dataclass
class Point:
	x: int
	y: int


@dataclass
class Symbol:
	position: Point
	value: str


@dataclass
class PartNumber:
	position: Point
	length: int
	value: int
	symbols: list[Symbol]


def draw_border(engine_schematic: list[str]) -> list[str]:
	"""
	Helper method for easier processing of input data. Border of dots of thickness = 1 is drawn to allow processing all
	adjacent points without the need for checking if index is out of range.
	:param engine_schematic: input engine schematic
	:return: engine schematic with added border
	"""
	for idx, schema_line in enumerate(engine_schematic):
		engine_schematic[idx] = '.' + engine_schematic[idx] + '.'
	engine_schematic = ['.' * len(engine_schematic[0])] + engine_schematic + ['.' * len(engine_schematic[0])]
	return engine_schematic


def parse_input() -> list[PartNumber]:
	"""
	Helper method to parse input board into list of part numbers with information on adjacent symbols and their position.
	For each part number, the search for an adjacent symbol is performed (iteration over fields around digits)
	:return: list of part numbers with information of position of the number, its value, details of adjacent symbols
	"""
	with open("./input.txt", "r") as f:
		engine_schematic = f.read().split("\n")
	engine_schematic = draw_border(engine_schematic)
	part_numbers = []
	for y in range(1, len(engine_schematic) - 1):
		x = 0
		while x < len(engine_schematic[0]):
			if not engine_schematic[y][x].isdigit():
				x += 1
			else:
				num_end = x
				while engine_schematic[y][num_end + 1].isdigit():
					num_end += 1
				surrounding_indexes = ([(x - 1, y), (num_end + 1, y)] +
									   [(xx, y - 1) for xx in range(x - 1, num_end + 2)] +
									   [(xx, y + 1) for xx in range(x - 1, num_end + 2)])
				surrounding = [engine_schematic[yy][xx] for xx, yy in surrounding_indexes]
				number = engine_schematic[y][x:num_end + 1]
				special_symbols = [
					Symbol(position=Point(x=surrounding_indexes[idx][0],
										  y=surrounding_indexes[idx][1]),
						   value=symbol
						   ) for idx, symbol in enumerate(surrounding) if symbol != '.'
				]
				part_numbers.append(PartNumber(
					position=Point(x=x, y=y),
					length=num_end - x + 1,
					value=int(number),
					symbols=special_symbols
				))
				x = num_end + 1
	return part_numbers


def part_one(part_numbers: list[PartNumber]) -> int:
	return sum([part_number.value for part_number in part_numbers if len(part_number.symbols) > 0])


def part_two(part_numbers: list[PartNumber]) -> int:
	asterix_adjacent_numbers = [(part_number.position, part_number.value, symbol.position)
								for part_number in part_numbers
								for symbol in part_number.symbols
								if symbol.value == "*"]
	numbers_for_asterix = defaultdict(set)
	for part_number_position, part_number_value, symbol_position in asterix_adjacent_numbers:
		numbers_for_asterix[f"{symbol_position.x}_{symbol_position.y}"].add(f"{part_number_position.x}_{part_number_position.y}_{part_number_value}")
	gears_candidates = [numbers for _, numbers in numbers_for_asterix.items() if len(numbers) > 1]
	gears_sum = sum(reduce((lambda x, y: x * y), [int(number.split("_")[2]) for number in numbers]) for numbers in gears_candidates)
	return gears_sum


if __name__ == "__main__":
	input_part_numbers = parse_input()
	print(f"Part one: {part_one(part_numbers=input_part_numbers)}")
	print(f"Part two: {part_two(part_numbers=input_part_numbers)}")
