
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import util

class SearchProblem:
   """
   This class outlines the structure of a search problem, but doesn't implement
   any of the methods (in object-oriented terminology: an abstract class).

   You do not need to change anything in this class, ever.
   """

   def getStartState(self):
       """
       Returns the start state for the search problem.
       """
       util.raiseNotDefined()

   def isGoalState(self, state):
       """
         state: Search state

       Returns True if and only if the state is a valid goal state.
       """
       util.raiseNotDefined()

   def getSuccessors(self, state):
       """
         state: Search state

       For a given state, this should return a list of triples, (successor,
       action, stepCost), where 'successor' is a successor to the current
       state, 'action' is the action required to get there, and 'stepCost' is
       the incremental cost of expanding to that successor.
       """
       util.raiseNotDefined()

   def getCostOfActions(self, actions):
       """
        actions: A list of actions to take

       This method returns the total cost of a particular sequence of actions.
       The sequence must be composed of legal moves.
       """
       util.raiseNotDefined()


def tinyMazeSearch(problem):
   """
   Returns a sequence of moves that solves tinyMaze.  For any other maze, the
   sequence of moves will be incorrect, so only use this for tinyMaze.
   """
   from game import Directions
   s = Directions.SOUTH
   w = Directions.WEST
   return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
   """
   Search the deepest nodes in the search tree first.

   Your search algorithm needs to return a list of actions that reaches the
   goal. Make sure to implement a graph search algorithm.

   To get started, you might want to try some of these simple commands to
   understand the search problem that is being passed in:

      """
   stack = util.Stack()  # holy fuck I finally found out how to do it, that took over an hour
   visited = []
   if not problem.isGoalState(problem.getStartState()):
       for item in problem.getSuccessors(problem.getStartState()):
           stack.push([item[0], item[1]])
   else:
       return []
   #okay, we have the first items on the stack
   while True:
       checking = stack.pop()  # this is a list with the items, eg. [(33, 16), 'West']
       list = checking[1]
       visited.append(checking[0])
       if problem.isGoalState(checking[0]):  # if what you're checking is a goal, then return the directions you've accrued
           return checking[1].split(" ")
       else: #case of you need to add stuff on the fringe (if necessary)
           for item in problem.getSuccessors(checking[0]):
               if item[0] not in visited:
                   tempList = list
                   tempList += " " + item[1]
                   stack.push([item[0], tempList])
           continue
       #every time, we need to get the tuples successors, depending on the direction you came from, never put on a place you've already seen
   #while(True):

   from game import Directions
   s = Directions.SOUTH
   w = Directions.WEST
   n = Directions.NORTH
   e = Directions.EAST
   return [s, s, w, s, w, w, s, w]
   util.raiseNotDefined()

def breadthFirstSearch(problem):
   stack = util.Queue()  # this is litteraly the same as dfs but it's a Queue
   visited = []
   if not problem.isGoalState(problem.getStartState()):
       visited.append(problem.getStartState())
       for item in problem.getSuccessors(problem.getStartState()):
           visited.append(item[0])
           stack.push([item[0], item[1]])
   else:
       return []
   #okay, we have the first items on the stack
   while True:
       checking = stack.pop()  # this is a list with the items, eg. [(33, 16), 'West']
       list = checking[1]
       if problem.isGoalState(checking[0]):  # if what you're checking is a goal, then return the directions you've accrued
           return checking[1].split(" ")
       else: #case of you need to add stuff on the fringe (if necessary)
           for item in problem.getSuccessors(checking[0]):
               if item[0] not in visited:
                   tempList = list
                   visited.append(item[0])
                   tempList += " " + item[1]
                   stack.push([item[0], tempList])
           continue
   util.raiseNotDefined()

def uniformCostSearch(problem):
   stack = util.PriorityQueue()  # holy fuck I finally found out how to do it, that took over an hour
   visited = []
   dict = {}
   #TODO: make it so I can put the fringe and dfs searching all in this class, that fixes passby reference
   if not problem.isGoalState(problem.getStartState()):
       visited.append(problem.getStartState())
       dict[problem.getStartState()] = 0
       for item in problem.getSuccessors(problem.getStartState()):
           visited.append(item[0]);
           dict[item[0]] = problem.getCostOfActions([item[1]]) #this adds the cost to the dictionary
           stack.push([item[0], item[1]], problem.getCostOfActions([item[1]]))
   else:
       return []
   #okay, we have the first items on the stack
   while True:
       #TODO: add cost idea, not just distance but path cost.
       checking = stack.pop()  # this is a list with the items, eg. [(33, 16), 'West']
       list = checking[1]
       if problem.isGoalState(checking[0]):  # if what you're checking is a goal, then return the directions you've accrued
           return checking[1].split(" ")
       else: #case of you need to add stuff on the fringe (if necessary)
           for item in problem.getSuccessors(checking[0]):
               tempList = list
               tempList += " " + item[1]
               if item[0] not in visited: #if we have not seen this state yet
                   visited.append(item[0])
                   dict[item[0]] = problem.getCostOfActions(tempList.split(" "))
                   stack.push([item[0], tempList], problem.getCostOfActions(tempList.split(" ")))
               elif dict[item[0]] > problem.getCostOfActions(tempList.split(" ")):
                   dict[item[0]] = problem.getCostOfActions(tempList.split(" "))
                   stack.push([item[0], tempList], problem.getCostOfActions(tempList.split(" ")))
           continue

def nullHeuristic(state, problem=None):
   """
   A heuristic function estimates the cost from the current state to the nearest
   goal in the provided SearchProblem.  This heuristic is trivial.
   """
   return 0


def aStarSearch(problem, heuristic=nullHeuristic):
   stack = util.PriorityQueue()  # holy fuck I finally found out how to do it, that took over an hour
   visited = []
   dict = {}
   # TODO: make it so I can put the fringe and dfs searching all in this class, that fixes passby reference
   if not problem.isGoalState(problem.getStartState()):
       visited.append(problem.getStartState())
       dict[problem.getStartState()] = 0
       for item in problem.getSuccessors(problem.getStartState()):
           visited.append(item[0]);
           dict[item[0]] = problem.getCostOfActions([item[1]])  # this adds the cost to the dictionary
           stack.push([item[0], item[1]], problem.getCostOfActions([item[1]])+heuristic(item[0], problem))
   else:
       return []
   # okay, we have the first items on the stack
   while True:
       # TODO: add cost idea, not just distance but path cost.
       checking = stack.pop()  # this is a list with the items, eg. [(33, 16), 'West']
       list = checking[1]
       if problem.isGoalState(checking[0]):  # if what you're checking is a goal, then return the directions you've accrued
           return checking[1].split(" ")
       else:  # case of you need to add stuff on the fringe (if necessary)
           for item in problem.getSuccessors(checking[0]):
               tempList = list
               tempList += " " + item[1]
               if item[0] not in visited:  # if we have not seen this state yet
                   visited.append(item[0])
                   dict[item[0]] = problem.getCostOfActions(tempList.split(" "))
                   stack.push([item[0], tempList], problem.getCostOfActions(tempList.split(" "))+heuristic(item[0], problem))
               elif dict[item[0]] > problem.getCostOfActions(tempList.split(" ")):
                   dict[item[0]] = problem.getCostOfActions(tempList.split(" "))
                   stack.push([item[0], tempList], problem.getCostOfActions(tempList.split(" "))+heuristic(item[0], problem))
           continue

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch



