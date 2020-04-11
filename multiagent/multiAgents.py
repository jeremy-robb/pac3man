# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions

import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print(bestIndices)
        chosenIndex = bestIndices[0]  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # print("This is current: ", currentGameState.getPacmanPosition())
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print("This is the successor: ", successorGameState.getPacmanPosition())
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print("Ghost state is: ", newGhostStates[0].getPosition())
        # print("Ghosts planned move is: ", newGhostStates[0].getDirection())
        # print("My planned state is: ", newPos)
        badMoves = []
        for i in range(len(newGhostStates)):
            dontGo = list(newGhostStates[i].getPosition())
            left = list(dontGo)
            right = list(dontGo)
            up = list(dontGo)
            down = list(dontGo)
            left[1] -= 1
            right[1] += 1
            up[0] += 1
            down[0] += -1
            badMoves.append(dontGo)
            badMoves.append(left)
            badMoves.append(right)
            badMoves.append(up)
            badMoves.append(down)
        # print("These are all the places you for sure dont want to be in: ", badMoves)
        # print("This is where I plan to go: ", list(newPos))
        # print("is my move bad? ", list(newPos) in badMoves)
        if list(newPos) in badMoves:
            # print("RUN AWAY")
            return -10000
        if action == 'Stop':
            return -9999
        # print("Time to look for food")
        # print("I am here: ", newPos, " Heres the food: ", currentGameState.getFood().asList())
        if newPos in currentGameState.getFood().asList():
            # print("I FOUND FOOD")
            return 1000
        min = -1000
        for i in newFood.asList():  # this gives me some small negative number, the bigger distance the worse it is
            # print("So im here: ", newPos, " and the food is here: ", i, " I am this close to the food: ", manhattanDistance(newPos, i)*-1)
            min = max(manhattanDistance(newPos, i) * -1, min)
        # print("The closest food is: ", min, " away")
        return min


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.


          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # print("agent numbers is: ", gameState.getNumAgents())
        """
        while there's still depth left to check keep going
        
        
        """
        m = -1000000000
        max = -100000000
        direction = ""
        for i in gameState.getLegalActions(0):
            m = self.minValue(1, gameState.generateSuccessor(0, i),
                              0)  # I start depth at 0 since I'm counting up to the final depth
            if m > max:
                max = m  # this is what I came up with to decide what direction to do in the end
                direction = i
                # print("Max is now ", max)
        return direction

    def maxValue(self, num, state, depth):  # you always know that this will be pacman, as defined by the problem
        if depth == self.depth:
            return self.evaluationFunction(state)  # case where depth is reached
        if len(state.getLegalActions()) == 0:
            return self.evaluationFunction(
                state)  # case where I litteraly cannot move, this may break if there's ghosts all around me (may freeze the game)
        v = -100000
        for i in state.getLegalActions(num):
            v = max(v, self.minValue(1, state.generateSuccessor(num, i),
                                     depth))  # I use 1 since I know this is pacman, if there's no ghosts this may fuck up
        return v

    def minValue(self, num, state, depth):
        v = 100000
        if len(state.getLegalActions(
                num)) == 0:  # I believe one of the ghosts is getting stuck because I keep getting 100000 as an answer
            return self.evaluationFunction(state)  # this is the fix

        if num == state.getNumAgents() - 1:  # for the last agent, since it's going to counter pacman (who choses max)
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
                v = min(v, self.maxValue(0, state.generateSuccessor(num, i),
                                         depth + 1))  # depth +1 because this is one ply complete
        else:
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
                v = min(v, self.minValue(num + 1, state.generateSuccessor(num, i), depth))
        return v
    # for each ghost there is, choose the minimum state there is
    # at the end of them choosing all the minimum states if I can make it a list, I should return the max of them
    # the only problem is that it's depth 1... how will I implement this to repeat?


"""
    def value(self, first, state):
        print("GOT TO VALUE")
        # If the state is terminal then return its utility
        if self.depth == 0:
            return self.evaluationFunction
        for i in state.getLegalActions(range(state.getNumAgents())):  # 0 - end
            if i == 0:
                if not first:
                    return self.maxValue(i, state)
            else:
                return self.minValue(i, state)
        # if the next agent is MAX (agent zero) then use max-value
        # if the next agent is MIN then return min-value
"""


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    globalDepth = 0

    def getAction(self, gameState):
        self.globalDepth = self.depth
        # print("Num 1 depth is: ", self.globalDepth)
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        m = 0
        max = -100000000
        direction = ""
        # for i in gameState.getLegalActions(0):
        #   m = self.minValue(1, gameState.generateSuccessor(0, i), 0, -100000, 100000)  # I start depth at 0 since I'm counting up to the final depth
        # I need to somehow remember the minmax for other states I think??
        #   if m > max:
        #       max = m  # this is what I came up with to decide what direction to do in the end
        #       direction = i
        # print("Max is now ", max)
        x = self.maxValue(0, gameState, 0, -1000000, 100000)
        #  print("-----------------------------")
        return x

    def maxValue(self, num, state, depth, a, b):  # you always know that this will be pacman, as defined by the problem
        bAction = "glitch"
        # print("My depth in max is now: ", depth)
        if state.isLose() or state.isWin():  # I got this as a suggestion on what to do, I figured this was the same as my next if statement but I'm adding it anyways
            # i.e. I have no clue where I got this method, or why it is needed (also it never changed my code but I'm keeping it)
            return self.evaluationFunction(state)
        # print("passed win loss, returning pacmans moves")
        if len(state.getLegalActions()) == 0:
            return self.evaluationFunction(
                state)  # case where I litteraly cannot move, this may break if there's ghosts all around me (may freeze the game)
        v = -100000
        score = v  # setting this as a best counter
        for i in state.getLegalActions(num):
            v = self.minValue(1, state.generateSuccessor(0, i), depth, a,
                              b)  # I use 1 since I know this is pacman, if there's no ghosts this may fuck up
            if v > score:
                score = v
                bAction = i
            #  if v > b:
            #     return v
            a = max(a, score)
            if score > b:
                return score
        # if a >= b:
        #    break;

        if depth == 0:
            return bAction  # case where depth is reached
        return score

    def minValue(self, num, state, depth, a, b):
        # print("received depth: ", depth, " in min")
        if state.isLose() or state.isWin():  # refer above in maxValue for an explanation on this
            return self.evaluationFunction(state)
        v = 100000
        # print("passed win loose in min")
        score = v
        # if len(state.getLegalActions(num)) == 0:  # I believe one of the ghosts is getting stuck because I keep getting 100000 as an answer
        #    return self.evaluationFunction(state) # this is the fix
        # print("num 2 global depth is: ", self.globalDepth)
        if num == state.getNumAgents() - 1:  # for the last agent, since it's going to counter pacman (who choses max)
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
                if depth + 1 == self.globalDepth:
                    v = self.evaluationFunction(state.generateSuccessor(num, i))
                else:
                    # print("Going back to pacman")
                    v = self.maxValue(0, state.generateSuccessor(num, i), depth + 1, a,
                                      b)  # depth +1 because this is one ply complete\
                if v < score:
                    score = v
                # print("Set v to anew")

                #  if v < a:
                #   return v
                b = min(b, score)
                if score < a:
                    return score
            #   if a >= b:
            #    break;
        else:
            #  print("Watching other ghosts move")
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
                v = self.minValue(num + 1, state.generateSuccessor(num, i), depth, a, b)
                if v < score:
                    score = v
                #   if v < a:
                #     return v
                b = min(b, score)
                if score < a:
                    return score
            # if a >= b:
            #    break;
        # print("Returning final score min")
        return score


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    globalDepth = 0

    def getAction(self, gameState):
        #print("using ex")
        self.globalDepth = self.depth
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        m = 0
        max = -100000000
        direction = ""
        # for i in gameState.getLegalActions(0):
        #   m = self.minValue(1, gameState.generateSuccessor(0, i), 0, -100000, 100000)  # I start depth at 0 since I'm counting up to the final depth
        # I need to somehow remember the minmax for other states I think??
        #   if m > max:
        #       max = m  # this is what I came up with to decide what direction to do in the end
        #       direction = i
        # print("Max is now ", max)
        x = self.maxValue(0, gameState, 0)
        #  print("-----------------------------")
        return x

    def maxValue(self, num, state, depth):  # you always know that this will be pacman, as defined by the problem
        bAction = "glitch"
        # print("My depth in max is now: ", depth)
        if state.isLose() or state.isWin():  # I got this as a suggestion on what to do, I figured this was the same as my next if statement but I'm adding it anyways
            # i.e. I have no clue where I got this method, or why it is needed (also it never changed my code but I'm keeping it)
            return self.evaluationFunction(state)
        # print("passed win loss, returning pacmans moves")
      #  if len(state.getLegalActions()) == 0:
          #  return self.evaluationFunction(state)  # case where I litteraly cannot move, this may break if there's ghosts all around me (may freeze the game)
        v = -100000
        score = v  # setting this as a best counter
        for i in state.getLegalActions(num):
            v = self.minValue(1, state.generateSuccessor(0, i), depth)  # I use 1 since I know this is pacman, if there's no ghosts this may fuck up
            if v > score:
                score = v
                bAction = i
        #  if v > b:
        #     return v
        # if a >= b:
        #    break;

        if depth == 0:
            return bAction  # case where depth is reached
        return score

    def minValue(self, num, state, depth):
        # print("received depth: ", depth, " in min")
        if state.isLose():  # refer above in maxValue for an explanation on this
            return self.evaluationFunction(state)
        v = 100000
        # print("passed win loose in min")
        score = v
        if len(state.getLegalActions(num)) == 0:  # I believe one of the ghosts is getting stuck because I keep getting 100000 as an answer
            return 100000 # this is the fix
        # print("num 2 global depth is: ", self.globalDepth)
        #print("Num agents is: ", state.getNumAgents(), " and num is ", num)
        if num == (state.getNumAgents() - 1):  # for the last agent, since it's going to counter pacman (who choses max)
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
               # print("depth is, ", depth, " and global depth is ", self.globalDepth)
                if depth + 1 == self.globalDepth:
                   # print("Hit mark")
                    v = self.evaluationFunction(state.generateSuccessor(num, i))
                    score += v
                else:
                    # print("Going back to pacman")
                    v = self.maxValue(0, state.generateSuccessor(num, i), depth + 1)  # depth +1 because this is one ply complete\
                    score += v
        else:
            #  print("Watching other ghosts move")
            for i in state.getLegalActions(num):  # if there's no legal actions then this million is returned
                v = self.minValue(num + 1, state.generateSuccessor(num, i), depth)
                score += v
            #   if v < a:
            #     return v
            # if a >= b:
            #    break;
        # print("Returning final score min")
        return score / len(state.getLegalActions(num))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
