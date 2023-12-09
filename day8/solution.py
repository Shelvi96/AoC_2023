import re
from dataclasses import dataclass


@dataclass
class Map:
	instruction: str
	network: dict[str, (str, str)]


@dataclass
class NodesStats:
	cycle_length: int
	terminal_nodes_occurrence: list[int]


def parse_input_graph() -> Map:
	with open("./input.txt", "r") as f:
		lines = f.read()
	instruction_regex = r"[LR]+"
	network_regex = r"([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)"
	instruction = re.search(instruction_regex, lines)[0]
	network = {
		single_instruction.group(1): (single_instruction.group(2), single_instruction.group(3))
		for single_instruction in re.finditer(network_regex, lines)
	}
	return Map(
		instruction=instruction,
		network=network
	)


def part_one(input_map: Map, starting_node: str, target_node: str) -> int:
	current_node = starting_node
	instruction_idx = 0
	steps_count = 0
	while current_node != target_node:
		current_node = input_map.network[current_node][0] \
			if input_map.instruction[instruction_idx] == "L" \
			else input_map.network[current_node][1]
		steps_count += 1
		instruction_idx = (instruction_idx + 1) % len(input_map.instruction)
	return steps_count


def part_two(input_map: Map) -> int:
	pass


if __name__ == "__main__":
	input_map: Map = parse_input_graph()
	print(f"Part one: {part_one(input_map=input_map, starting_node='AAA', target_node='ZZZ')}")
	print(f"Part two: {part_two(input_map=input_map)}")
