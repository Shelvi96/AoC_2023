CONVERTING_RULES = {
	'one': '1',
	'two': '2',
	'three': '3',
	'four': '4',
	'five': '5',
	'six': '6',
	'seven': '7',
	'eight': '8',
	'nine': '9',
}


def part_one(calibration_values: list[str]) -> int:
	calibration_sum = 0
	for line in calibration_values:
		digits = [char for char in line if char.isdigit()]
		if len(digits) == 0:
			raise ValueError
		else:
			calibration_sum += int(digits[0] + digits[-1])
	return calibration_sum


def part_two(calibration_values: list[str]) -> int:
	calibration_sum = 0
	for line in calibration_values:
		for key, value in CONVERTING_RULES.items():
			line = line.replace(key, key + value + key)
		digits = [char for char in line if char.isdigit()]
		if len(digits) == 0:
			raise ValueError
		else:
			calibration_sum += int(digits[0] + digits[-1])
	return calibration_sum


if __name__ == "__main__":
	with open("./input.txt", "r") as f:
		calibration_values = f.readlines()
	print(f"Part one: {part_one(calibration_values=calibration_values)}")
	print(f"Part two: {part_two(calibration_values=calibration_values)}")
