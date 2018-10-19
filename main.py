# CS480 Project 3
# Created by: Elias Mote and Justin Ramos
# Date: 10/18/18


import datetime, heapq


def main():
	# Get the permutation from user input
	permutation = get_input()

	DoAStarGraphWork(permutation)


def DoAStarGraphWork(permutation):
	print("Starting A* Graph Search")
	startTime = datetime.datetime.now()

	# Create our starting node
	start = Node(h(permutation), permutation, 0, [])
	# Give starting node to A*, start the A* search
	res, solutionNode, maxqsize, totalvisitedstates = AStarGraph(start)

	endTime = datetime.datetime.now()

	if(res):
		solutionPath = []

		# Following the pointers backwards until we arrive at the
		# root node, which is the only node with a parent of [].
		while(solutionNode != []):
			solutionPath.append(solutionNode.key)
			solutionNode = solutionNode.parent

		# Reverse the solution path.
		solutionPath = solutionPath[::-1]

		print("Path to solution:")
		for i in solutionPath:
			print(i)

		# Print out statistics
		elapsedTime = endTime - startTime
		print("CPU time: " + str(float(elapsedTime.seconds) + float(elapsedTime.microseconds) / 1000000) + " second(s)")
		print("Total visited states: " + str(totalvisitedstates))
		print("Max queue size: " + str(maxqsize))
	else:
		# We shouldn't actually get here but whatever.
		print("No solution found")


def AStarGraph(start):
	maxqsize = 0
	totalvisitedstates = 0

	heap = []
	closedSet = {}
	openSet = {}

	# Add starting node to heap and open set
	heapq.heappush(heap, start)
	# The key in our open set will be the hash of the node's key turned into a string
	openSet[start.key.__str__()] = start

	maxqsize += 1

	while(len(openSet) > 0):
		# Adjust our stats
		if(len(heap) > maxqsize):
			maxqsize = len(heap)
		totalvisitedstates += 1


		currentNode = heapq.heappop(heap)
		# Cycle through invalid nodes. We do this because Python's heapq implementation does not have
		# a decreaseKey function. So we just mark the node as invalid and push another into the heap.
		while(currentNode.invalid):
			currentNode = heapq.heappop(heap)

		# Add the current node to the closed set and remove it from the open set.
		closedSet[currentNode.key.__str__()] = currentNode
		openSet.pop(currentNode.key.__str__())

		# Check if the node's key is in the form 1, 2, 3, ..., n, indicating we've found a solution.
		if(IsValid(currentNode.key)):
			return True, currentNode, maxqsize, totalvisitedstates
		else:
			for newKey in GenerateSuccessors(currentNode.key):
				# Avoid cycles of length 2 by not trying to add a new node if the key of the new node
				# is the same as the parent of the current node.
				if(newKey != currentNode.parent):
					# Try to improve existing connections in the open set, or improve and re-add nodes from
					# the closed set, or add a completely new node into the open set.
					Improve(openSet, closedSet, heap, currentNode, newKey)

	# Getting here indicates we did not find a solution.
	return False, None, maxqsize, totalvisitedstates


def Improve(openSet, closedSet, heap, currentNode, newKey):
	# If the node is already in our open set, check to see if we've got a better path
	if(newKey.__str__() in openSet):
		if(currentNode.distance + 1 < openSet[newKey.__str__()].distance):
			# If we have a better path, then we need to make sure we use this new path instead of the old path.

			# Python's heapq implementation does not have a decreaseKey function. Instead we'll set a flag on the node
			# to True. The flag is called "invalid." When we pop the min node from a heap and it is invalid then we'll
			# simply ignore it and just pop the next min node.
			openSet[newKey.__str__()].SetAsInvalid()

			# We'll push a new node to the heap with the better distance value. We'll also re-add the node to the
			# open set.
			newNode = Node(currentNode.distance + 1 + h(newKey), newKey, currentNode.distance + 1, currentNode)
			openSet[newKey.__str__()] = newNode
			heapq.heappush(heap, newNode)

	# If the node was previously removed from the open set and is now closed, we want to check to see if we've now
	# found a better path to that node which we can expand on.
	elif(newKey.__str__() in closedSet):
		if(currentNode.distance + 1 < closedSet[newKey.__str__()].distance):

			# Update the node's distance value with a better path and update the parent with the new parent.
			closedSet[newKey.__str__()].parent = currentNode
			closedSet[newKey.__str__()].distance = currentNode.distance + 1 + h(newKey)

			# Add the node to the open set
			openSet[newKey.__str__()] = closedSet[newKey.__str__()]

			# Remove the node from the closed set
			closedSet.pop(newKey.__str__())

			# Re-add the node to the heap
			heapq.heappush(heap, openSet[newKey])

	# If we've encountered a never-before-seen state, create a new node and add it to the open set and heap.
	else:
		newNode = Node(currentNode.distance + 1 + h(newKey), newKey, currentNode.distance + 1, currentNode)
		openSet[newKey.__str__()] = newNode
		heapq.heappush(heap, newNode)


class Node:
	def __init__(self, priority, key, distance, parent):
		self.priority = priority
		self.key = key
		self.distance = distance
		self.parent = parent
		self.invalid = False

	# We implement this so the heapq module can properly insert and pop elements from the heap
	def __lt__(self, other):
		return self.priority < other.priority

	# Used to determine if we should ignore this node or not
	def SetAsInvalid(self):
		self.invalid = True


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


# Generates the successors of a key and yields them to the caller.
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


# Checks if a key is in ascending order
def IsValid(key):
	lastNum = -1

	for currentNum in key:
		if(lastNum > currentNum):
			return False
		lastNum = currentNum
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
