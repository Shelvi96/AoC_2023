import re
from dataclasses import dataclass

SEED_REGEX = r"(?s)(?<=seeds: )(.*?)(?=\n\n)"
CONVERSION_REGEX = {
	"seed_to_soil": r"(?s)(?<=seed-to-soil map:\n)(.*?)(?=\n\n)",
	"soil_to_fertilizer": r"(?s)(?<=soil-to-fertilizer map:\n)(.*?)(?=\n\n)",
	"fertilizer_to_water": r"(?s)(?<=fertilizer-to-water map:\n)(.*?)(?=\n\n)",
	"water_to_light": r"(?s)(?<=water-to-light map:\n)(.*?)(?=\n\n)",
	"light_to_temperature": r"(?s)(?<=light-to-temperature map:\n)(.*?)(?=\n\n)",
	"temperature_to_humidity": r"(?s)(?<=temperature-to-humidity map:\n)(.*?)(?=\n\n)",
	"humidity_to_location": r"(?s)(?<=humidity-to-location map:\n)(.*)"
}
PARAMETERS = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


@dataclass
class ConversionRule:
	convert_from: str
	convert_to: str
	conversion_regex: re.Pattern


@dataclass
class Interval:
	source: int
	target: int
	step: int


@dataclass
class Conversion:
	rule: ConversionRule
	intervals: list[Interval]


@dataclass
class Almanac:
	seeds: list[int]
	conversions: list[Conversion]


def parse_intervals(lines: str, rule: re.Pattern) -> list[Interval]:
	lines = re.findall(rule, lines)[0].split("\n")
	lines = [line.split(" ") for line in lines]
	return [
		Interval(
			source=int(line[1]),
			target=int(line[0]),
			step=int(line[2])
		) for line in lines
	]


def parse_almanac() -> Almanac:
	with open("input.txt") as f:
		lines = f.read()
	conversion_rules = [
		ConversionRule(
			convert_from=convert_from,
			convert_to=convert_to,
			conversion_regex=CONVERSION_REGEX[f"{convert_from}_to_{convert_to}"]
		)
		for convert_from, convert_to in zip(PARAMETERS[:-1], PARAMETERS[1:])
	]
	conversions = [
		Conversion(
			rule=rule,
			intervals=parse_intervals(lines=lines, rule=rule.conversion_regex)
		) for rule in conversion_rules
	]
	seeds = list(map(int, re.findall(SEED_REGEX, lines)[0].split(" ")))
	return Almanac(
		seeds=seeds,
		conversions=conversions
	)


def part_one(almanac: Almanac) -> int:
	seeds_locations = []
	for seed in almanac.seeds:
		current_value = seed
		conversion_rules_to_intervals = {
			f"{interval.rule.convert_from}_{interval.rule.convert_to}": interval
			for interval in almanac.conversions
		}
		for parameter, next_parameter in zip(PARAMETERS[:-1], PARAMETERS[1:]):
			current_conversion = conversion_rules_to_intervals[f"{parameter}_{next_parameter}"]
			for interval in current_conversion.intervals:
				if interval.source <= current_value < interval.source + interval.step:
					current_value += interval.target - interval.source
					break
		seeds_locations.append(current_value)
	return min(seeds_locations)


def part_two(almanac: Almanac) -> int:
	seed_intervals = [
		(seed, seed+seed_range)
		for seed, seed_range in zip(almanac.seeds[::2], almanac.seeds[1::2])
	]
	# TODO
	return 0


if __name__ == "__main__":
	input_almanac: Almanac = parse_almanac()
	print(f"Part one: {part_one(almanac=input_almanac)}")
	print(f"Part two: {part_two(almanac=input_almanac)}")
