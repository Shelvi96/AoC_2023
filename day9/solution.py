import re


def part_one(values_history: list[list[int]]) -> int:
	sum_of_predictions = []
	for value_history in values_history:
		value_history_step = value_history
		last_from_step = [value_history_step[-1]]
		while set(value_history_step) != {0}:
			value_history_step = [v2 - v1 for v1, v2 in zip(value_history_step[:-1], value_history_step[1:])]
			last_from_step.append(value_history_step[-1])
		sum_of_predictions.append(sum(last_from_step))
	return sum(sum_of_predictions)


def part_two(values_history: list[list[int]]) -> int:
	sum_of_predictions = []
	for value_history in values_history:
		value_history_step = value_history
		first_from_step = [value_history_step[0]]
		while set(value_history_step) != {0}:
			value_history_step = [v2 - v1 for v1, v2 in zip(value_history_step[:-1], value_history_step[1:])]
			first_from_step.append(value_history_step[0])
		cur_pred_val = 0
		for val in first_from_step[::-1]:
			cur_pred_val = val - cur_pred_val
		sum_of_predictions.append(cur_pred_val)
	return sum(sum_of_predictions)


def parse_input() -> list[list[int]]:
	with open("./input.txt", "r") as f:
		values_history = [
			[int(number[0]) for number in re.finditer(r"[0-9\-]+", line)]
			for line in f.readlines()
		]
	return values_history


if __name__ == "__main__":
	input_values_history = parse_input()
	print(f"Part one: {part_one(values_history=input_values_history)}")
	print(f"Part two: {part_two(values_history=input_values_history)}")
