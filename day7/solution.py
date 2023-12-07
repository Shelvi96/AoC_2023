import enum
from dataclasses import dataclass

CARDS_ORDER_DESC_1 = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_ORDER_DESC_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
CARDS_WEIGHTS_DESC = ["m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a"]


class HandType(enum.Enum):
	"""
	Class for representing hand type (a set of cards in hand)
	"""
	FIVE_OF_A_KIND = 6
	FOUR_OF_A_KIND = 5
	FULL_HOUSE = 4
	THREE_OF_A_KIND = 3
	TWO_PAIR = 2
	ONE_PAIR = 1
	HIGH_CARD = 0

	def __lt__(self, other):
		return self.value < other.value


@dataclass
class Hand:
	"""
	Class representing player's hand (type of hand, cards, bid value)
	:param type: type of hand
	:param cards: string representing cards in hand
	:param cards_weighted: string representing cards with values transformed for convenient comparison between hands
	:param bid: bid value
	"""
	type: HandType
	cards: str
	cards_weighted: str
	bid: int

	def __gt__(self, other: "Hand"):
		if self.type == other.type:
			return self.cards_weighted > other.cards_weighted
		return self.type > other.type


class HandManager:
	"""
	HandManager class to handle operations on cards in hands, such as hand type classification or cards substitution.
	"""
	ALL_ACES_HAND: str = "AAAAA"  # most valuable hand

	@staticmethod
	def _parse_cards_to_cards_map(cards: str) -> dict:
		"""
		Helper method to parse cards in hand into a card occurence dictionary
		:param cards: string representing cards in hand
		:return: card occurence dictionary
		"""
		unique_chars = set(cards)
		return {
			char: cards.count(char) for char in unique_chars
		}

	@classmethod
	def classify_hand(cls, cards: str) -> HandType:
		"""
		Method to classify hand type (full house, two pair, etc.) based on cards in hand.
		Possible card combinations: AAAAA AAAAB AAABB AAABC AABBC AABCD ABCDE
		:return: HandType, type of hand (e.g. FULL_HOUSE, TWO_PAIR)
		"""
		cards_map = cls._parse_cards_to_cards_map(cards=cards)
		if len(cards_map) == 1:
			return HandType.FIVE_OF_A_KIND
		if len(cards_map) == 2 and min(cards_map.values()) == 2:
			return HandType.FULL_HOUSE
		if len(cards_map) == 2:
			return HandType.FOUR_OF_A_KIND
		if len(cards_map) == 3 and max(cards_map.values()) == 3:
			return HandType.THREE_OF_A_KIND
		if len(cards_map) == 3:
			return HandType.TWO_PAIR
		if len(cards_map) == 4:
			return HandType.ONE_PAIR
		return HandType.HIGH_CARD

	@classmethod
	def substitute_jokers(cls, cards: str) -> str:
		"""
		Method to substitute joker cards with most common non-joker card in hand. In case all cards are jokers, the
		method will substitute them with Aces.
		:param cards: string with cards
		:return: string representing cards in hand
		"""
		cards_map = cls._parse_cards_to_cards_map(cards=cards)
		non_joker_cards_map = {k: v for k, v in cards_map.items() if k != "J"}
		if len(non_joker_cards_map) == 0:  # all cards are jokers
			return cls.ALL_ACES_HAND
		max_occurence_non_joker_card = max(non_joker_cards_map, key=cards_map.get)
		return cards.replace("J", max_occurence_non_joker_card)

	@classmethod
	def get_cards_weighted(cls, cards: str, cards_order: list[str] | None = None) -> str:
		"""
		Method to convert cards into new cards set with corresponding letters representing weight of each card. This is
		used to conveniently compare hands with each other in case of same hand type.
		:param cards: string with cards
		:param cards_order: list representing cards order
		:return: weighted cards
		"""
		if cards_order is None:
			cards_order = CARDS_ORDER_DESC_1
		CARD_TO_WEIGHT_MAP = {
			card: weight for card, weight in zip(cards_order, CARDS_WEIGHTS_DESC)
		}
		return "".join([CARD_TO_WEIGHT_MAP[card] for card in cards])


def parse_input() -> list[Hand]:
	"""
	Method to load input from file and parse it into Hand objects.
	:return: list of Hand objects
	"""
	with open("./input.txt", "r") as f:
		lines = [line.split(" ") for line in f.readlines()]
		hands = [Hand(
			type=HandManager.classify_hand(cards=line[0]),
			cards=line[0],
			cards_weighted=HandManager.get_cards_weighted(cards=line[0]),
			bid=int(line[1])
		) for line in lines]
	return hands


def part_one(hands: list[Hand]) -> int:
	return sum([(order + 1) * hand.bid for order, hand in enumerate(sorted(hands))])


def part_two(hands: list[Hand]) -> int:
	for hand in hands:
		hand.cards_weighted = HandManager.get_cards_weighted(cards=hand.cards, cards_order=CARDS_ORDER_DESC_2)
		hand.cards = HandManager.substitute_jokers(cards=hand.cards)
		hand.type = HandManager.classify_hand(cards=hand.cards)
	return sum([(order + 1) * hand.bid for order, hand in enumerate(sorted(hands))])


if __name__ == "__main__":
	input_hands = parse_input()
	print(f"Part one: {part_one(hands=input_hands)}")
	print(f"Part two: {part_two(hands=input_hands)}")
