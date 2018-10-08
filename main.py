# CS480 Project 3
# Created by: Elias Mote and Justin Ramos
# Date: 10/5/18


import datetime, heapq


def main():
	# Get the permutation from user input
	permutation = [5, 4, 13, 1, 6, 2, 11, 108, 67] # get_input()

	DoAStarWork(permutation)


def DoAStarWork(permutation):
	print("Starting A* Search")
	startTime = datetime.datetime.now()

	res, parent = AStar(permutation)

	endTime = datetime.datetime.now()
	elapsedTime = endTime - startTime
	print("CPU time: " + str(float(elapsedTime.seconds) + float(elapsedTime.microseconds) / 1000000) + " second(s)")

	if(res):
		print("YES")
		solutionPath = []

		# The last node added to the parent array is our solution
		solution = parent[-1]
		# Following the pointers backwards until we arrive at the
		# root node, which is the only node with a parent of [].
		while(solution != []):
			solutionPath.append(solution.key)
			solution = solution.parent

		# Reverse the solution path.
		solutionPath = solutionPath[::-1]

		for i in solutionPath:
			print(i)
	else:
		print("NO")


def AStar(permutation):
	heap = []
	parent = []

	start = Node()
	start.priority = h(permutation)
	start.key = permutation
	start.distance = 0
	start.parent = []

	heapq.heappush(heap, start)

	while(len(heap) > 0):
		currentNode = heapq.heappop(heap)
		parent.append(currentNode)
		if(IsValid(currentNode.key)):
			return True, parent
		for successor in GenerateSuccessors(currentNode.key):
			if(successor != currentNode.parent):
				newNode = Node()
				newNode.priority = currentNode.distance + 1 + h(successor)
				newNode.key = successor
				newNode.distance = currentNode.distance + 1
				newNode.parent = currentNode

				heapq.heappush(heap, newNode)

	return False, []


class Node:
	def __init__(self):
		self.priority = -1
		self.key = []
		self.distance = -1
		self.parent = None

	def __lt__(self, other):
		return self.priority < other.priority


# Our heuristic is going to be half the number
# of breaks in the current permutation.
def h(permutation):
	return 0.5 * GetNumBreaks(permutation)


def GetNumBreaks(permutation):
	count = 0

	for i in range(len(permutation) - 1):
		# To be considered a break, the current number + 1 and
		# current number - 1 cannot equal the next number in the list.
		if (permutation[i] - 1 != permutation[i + 1] and permutation[i] + 1 != permutation[i + 1] and permutation[i] != permutation[i + 1]):
			count += 1

	return count


# Generated the successors of a key and yields them to the caller.
# A successor is a key where the first 0 to n entries are reversed.
# n > 2 and n < len(key)
# What we return is a new list consisting of the reversed portion
# at the front and the regular portion at the back.
def GenerateSuccessors(key):
	for i in range(0, len(key)):
		for j in range(i, len(key) + 1):
			newKeyStart = key[0:i]

			# We want to swap only from 0 to n.
			# The slice below will make a new list consisting of
			# elements 0 to i (not including element i).
			newKeyReversedMiddle = key[i:j]

			# Reverses that list.
			newKeyReversedMiddle = newKeyReversedMiddle[::-1]

			# Grid the elements from i to the end, where the end can
			# just be defined as the length of the key.
			newKeyEnd = key[j:len(key)]

			# Create a final list with the original start,
			# reversed middle and normal end.
			newKey = newKeyStart + newKeyReversedMiddle + newKeyEnd

			yield newKey


# Checks if a key is in the form 1, 2, 3, ... n
def IsValid(key):
	mMax = -1

	for i in key:
		if(mMax > i):
			return False
		mMax = i
	return True


# Get the permutation input from the user
def get_input():

	# Ask the user for an input permutation P
	permutation = input("Please enter input permutation: ")

	# Split the elements up
	permutation = permutation.split(' ')

	# Convert the strings of the permutation to integers
	for i in range(0,len(permutation)):
		permutation[i] = int(permutation[i])

	# Return the permutation
	return permutation








main()
