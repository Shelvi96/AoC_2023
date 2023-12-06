import math
from functools import reduce


def get_solution_interval(a: int, b: int) -> (float, float):
	"""
	Function returning soultion interval for inequality - x x + a x - b > 0 for given a, b
	:param a: inequality parameter, max race time
	:param b: inequality parameter, current distance record
	:return: inequality soultion interval
	"""
	return 0.5 * (a - pow(a * a - 4 * b, 0.5)), 0.5 * (a + pow(a * a - 4 * b, 0.5))


def get_natural_solutions_count(solution_interval: tuple[float, float]) -> float:
	"""
	Helper function returning number of integers in given interval
	:param solution_interval: float solution interval
	:return: a number of integers in given interval
	"""
	return math.floor(solution_interval[-1]) - math.ceil(solution_interval[0]) + 1


def part_one(time: list[int], distance: list[int]) -> float:
	"""
	The problem presented in today's task may be described as finding the number of solutions for following formula:
		-t_c^2 + t*t_c - s > 0,
	where t_c is charging time, t is race time, s is current record.
	Our objective is to beat the record, which will happen once our charging time t_c will be a solution for given formula.
	:param time: input time list
	:param distance: input distance list
	:return: product of sum of solutions for each test case
	"""
	return reduce(
		(lambda x, y: x * y),
		[get_natural_solutions_count(solution_interval=get_solution_interval(t, d)) for t, d in zip(time, distance)]
	)


def part_two(time: list[int], distance: list[int]) -> float:
	"""
	This is the same problem, except the input must be modified first.
	:param time: input time list
	:param distance: input distance list
	:return: number of solutions for modified test case
	"""
	time_parsed = int(''.join(map(str, time)))
	distance_parsed = int(''.join(map(str, distance)))
	return get_natural_solutions_count(solution_interval=get_solution_interval(time_parsed, distance_parsed))


if __name__ == "__main__":
	TIME = [46, 82, 84, 79]
	DISTANCE = [347, 1522, 1406, 1471]
	print(f"Part one: {part_one(time=TIME, distance=DISTANCE)}")
	print(f"Part two: {part_two(time=TIME, distance=DISTANCE)}")
