import random
from abc import ABC
from typing import List, T, Tuple

# ================================================
# 
# LISTS
# 
# ================================================
class MergeSortListComparator(ABC):
	"""Base class

	Extend this to create a comparator for use with merge sort list.
	"""
	@staticmethod
	def compare(a: List[T], b: List[T]) -> bool:
		pass

def mergeSortList(inputList: List[T], comparator: MergeSortListComparator) -> List[T]:
	"""Merge sort list

	Worst case performance O(n log n).
	
	Project layer must implement a custom MergeSortListComparator.
	
	Example:
	To sort myList=[4,3,2,1] into ascending order, MyComparator.compare
	implementation would be:
	return a[0] <= b[0]
	
	Call would be mergeSortList(myList, MyComparator())"""
	# Input validation
	if not type(inputList) is list:
		raise TypeError('inputList must be list.')
	if not isinstance(comparator, MergeSortListComparator):
		raise TypeError('comparator must be an instance of a sub class of MergeSortListComparator.')
	
	# If only one element, return
	if len(inputList) <= 1:
		return inputList

	if not type(comparator.compare(inputList, inputList)) is bool:
		raise TypeError('comparator.compare function must accept input list or a subset of input list and return bool.')

	left = []
	right = []

	# Split list
	for i, x in enumerate(inputList):
		if i < (len(inputList) / 2):
			left.append(x)
		else:
			right.append(x)

	# Sort halves
	left = mergeSortList(left, comparator)
	right = mergeSortList(right, comparator)

	# Merge halves
	return __mergeSortList_Merge(left, right, comparator)

def __mergeSortList_Merge(left: List[T], right: List[T], comparator: MergeSortListComparator) -> List[T]:
	result = []

	# Sort lists
	while len(left) != 0 and len(right) != 0:
		if comparator.compare(left, right):
			result.append(left[0])
			del left[0]
		else:
			result.append(right[0])
			del right[0]
		
	# Consume any remaining elements
	while len(left) != 0:
		result.append(left[0])
		del left[0]
	while len(right) != 0:
		result.append(right[0])
		del right[0]

	return result

# ------------------------------------------------

def shuffleList(inputList: List[T], iterations: int) -> List[T]:
	"""Shuffle list

	Randomly shuffles input list:
	1. Copy element at random index.
	2. Delete element at that index.
	3. Generate new random index.
	4. Insert copied element at new random index.
	5. Repeat iterations times."""
	# Input validation
	if not type(inputList) is list:
		raise TypeError('inputList must be list.')
	if not type(iterations) is int:
		raise TypeError('iterations must be int.')
	if iterations < 0:
		raise ValueError('iterations must be greater than 0')

	# Check if 0 iterations or empty list
	if(iterations == 0 or len(inputList) == 0):
		return inputList

	# Shuffle
	currentIteration = 0
	while currentIteration < iterations:
		# Select random member to move
		i = random.randint(0, len(inputList) - 1)
		element = inputList[i]

		# Delete current instance of member
		del inputList[i]

		# Select random position and insert
		j = random.randint(0, len(inputList) - 1)
		inputList.insert(j, element)

		# Increment current iteration
		currentIteration += 1

	return inputList

# ------------------------------------------------

def swapListElementRange(list1: List[T], list2: List[T], i1: int, i2: int) -> Tuple[List[T], List[T]]:
	"""Swap Element Range

	Swaps element range between two lists."""
	# Input validation
	if not type(list1) is list:
		raise TypeError('list1 must be list.')
	if not type(list2) is list:
		raise TypeError('list2 must be list.')
	if not type(i1) is int:
		raise TypeError('i1 must be int.')
	if not type(i2) is int:
		raise TypeError('i2 must be int.')
	if 0 > i1 >= len(list1) or 0 > i1 >= len(list2):
		raise IndexError('i1 must be within the bounds of list1 and list2')
	if 0 > i2 >= len(list1) or 0 > i2 >= len(list2):
		raise IndexError('i2 must be within the bounds of list1 and list2')

	# Swap
	for i in range(i1, i2):
		temp = list1[i]
		list1[i] = list2[i]
		list2[i] = temp

	return (list1, list2)