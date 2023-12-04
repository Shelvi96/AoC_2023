import re
import numpy as np
from dataclasses import dataclass


@dataclass
class Card:
	id: int
	winning_numbers: list[int]
	guessed_numbers: list[int]


def parse_number_list(numbers_str: str) -> list[int]:
	"""
	Helper method for parsing string containing numbers separated by whitespaces into list of numbers
	:param numbers_str: input string
	:return: output list of numbers
	"""
	numbers_list_cleared = [text for text in numbers_str.split(" ") if len(text) > 0]
	return list(map(int, numbers_list_cleared))


def parse_card(card: str) -> Card:
	"""
	Helper method to parse a single card (single input line)
	:param card: input line representing one card
	:return: Card object, a result of parsing
	"""
	card_id_candidates = re.findall(r"Card *(\d+):", card)
	card_id = int(card_id_candidates[0])
	numbers_set = card.split(":")[1]
	winning_numbers_str, guessed_numbers_str = numbers_set.split("|")

	return Card(
		id=card_id,
		winning_numbers=parse_number_list(winning_numbers_str),
		guessed_numbers=parse_number_list(guessed_numbers_str)
	)


def part_one(cards: list[Card]) -> int:
	cards_winning_count = [len(set(card.guessed_numbers).intersection(set(card.winning_numbers))) for card in cards]
	return sum(
		[pow(2, card_winning - 1) for card_winning in cards_winning_count if card_winning > 0]
	)


def part_two(cards: list[Card]) -> int:
	cards_copies = np.array([1] * (len(cards)))
	cards_winning_count = [len(set(card.guessed_numbers).intersection(set(card.winning_numbers))) for card in cards]
	for idx, card_winning_count in enumerate(cards_winning_count):
		cards_copies[idx+1:idx+1+card_winning_count] += cards_copies[idx]
	return sum(cards_copies)


if __name__ == "__main__":
	with open("./input.txt", "r") as f:
		cards = [parse_card(card=line) for line in f.readlines()]
	print(f"Part one: {part_one(cards=cards)}")
	print(f"Part two: {part_two(cards=cards)}")
