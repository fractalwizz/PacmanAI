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
import random, util, sys


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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        
        score = successorGameState.getScore()
        dist = 0;
        
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        if action == Directions.STOP:              # prefers empty space to stopping
            return score - 100
        
        if not currentGameState.getFood()[newPos[0]][newPos[1]]:
            dist = 9 - getClosestFood(newPos, newFood) # Get closest food
                
        #dist = 9 - getClosestFood(newPos, newFood) # Get closest food
        
        score += dist
        
        return score
            
def getClosestFood(pos, food):
    # compare manhattan distances
    min = ()
    dist = 9999
        
    for x in range(food.width):
        for y in range(food.height):
            temp = util.manhattanDistance(pos, (x,y))
            
            if food[x][y] and temp <= dist:
                min = (x,y)
                dist = temp
                
    return dist

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
            
          IDEA: getNumAgents determines the indices.
                start at self.index (0)
                passing along index to minimax
                in maxValue and minValue, increment index
                in recursive call, new index refers to next agent
                continue until index = getNumAgents()
                then index = 0 and depth++
        """
        "*** YOUR CODE HERE ***"
        
        legalMoves = gameState.getLegalActions(self.index)
        scores = [self.minimax(gameState.generateSuccessor(self.index, action), self.index + 1, 0) for action in legalMoves]
        
        bestScore = max(scores)
        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        
        return legalMoves[chosenIndex]
        
    def minimax(self, gameState, index, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
    
        if index == gameState.getNumAgents():
            "*** End of Depth ***"
            index = 0
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
                
        if index == 0:
            "*** MAX Agent ***"
            return self.maxValue(gameState, index, depth)
            
        if index > 0:
            "*** MIN Agent ***"
            return self.minValue(gameState, index, depth)
            
        
    def maxValue(self, gameState, index, depth):
        v = -sys.maxint - 1
        for action in gameState.getLegalActions(index):
            v = max(v, self.minimax(gameState.generateSuccessor(index, action), index + 1, depth))            
        return v
            
    def minValue(self, gameState, index, depth):
        v = sys.maxint
        for action in gameState.getLegalActions(index):
            v = min(v, self.minimax(gameState.generateSuccessor(index, action), index + 1, depth))      
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(self.index)
        #scores = [self.minimax(gameState.generateSuccessor(self.index, action), self.index + 1, 0, -sys.maxint - 1, sys.maxint) for action in legalMoves]
        
        alpha = -sys.maxint - 1
        beta = sys.maxint
        scores = [];
        for action in legalMoves:
            v = self.minimax(gameState.generateSuccessor(self.index, action), self.index + 1, 0, alpha, beta)
            scores.append(v)
            alpha = max(alpha, v)
        
        bestScore = max(scores)
        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        
        return legalMoves[chosenIndex]
        
    def minimax(self, gameState, index, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
    
        if index == gameState.getNumAgents():
            "*** End of Depth ***"
            index = 0
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
                
        if index == 0:
            "*** MAX Agent ***"
            return self.maxValue(gameState, index, depth, alpha, beta)
            
        if index > 0:
            "*** MIN Agent ***"
            return self.minValue(gameState, index, depth, alpha, beta)
            
        
    def maxValue(self, gameState, index, depth, alpha, beta):
        v = -sys.maxint - 1
        
        for action in gameState.getLegalActions(index):
            v = max(v, self.minimax(gameState.generateSuccessor(index, action), index + 1, depth, alpha, beta))
            
            if v > beta:
                return v

            alpha = max(alpha, v)
        return v
            
    def minValue(self, gameState, index, depth, alpha, beta):
        v = sys.maxint
        
        for action in gameState.getLegalActions(index):
            v = min(v, self.minimax(gameState.generateSuccessor(index, action), index + 1, depth, alpha, beta))
            
            if v < alpha:
                return v

            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(self.index)
        scores = [self.minimax(gameState.generateSuccessor(self.index, action), self.index + 1, 0) for action in legalMoves]
        
        bestScore = max(scores)
        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        
        return legalMoves[chosenIndex]
        
    def minimax(self, gameState, index, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
    
        if index == gameState.getNumAgents():
            "*** End of Depth ***"
            index = 0
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
                
        if index == 0:
            "*** MAX Agent ***"
            return self.maxValue(gameState, index, depth)
            
        if index > 0:
            "*** MIN Agent ***"
            return self.minValue(gameState, index, depth)
            
        
    def maxValue(self, gameState, index, depth):
        v = -sys.maxint - 1
        for action in gameState.getLegalActions(index):
            v = max(v, self.minimax(gameState.generateSuccessor(index, action), index + 1, depth))            
        return v
            
    def minValue(self, gameState, index, depth):
        v = 0
        length = len(gameState.getLegalActions(index))
        
        for action in gameState.getLegalActions(index):
            v += self.minimax(gameState.generateSuccessor(index, action), index + 1, depth)

        result = float(v / length)
        return result

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

