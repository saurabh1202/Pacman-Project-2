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
        #print("successorGameState = ",successorGameState)
        newPos = successorGameState.getPacmanPosition()
        #print("newPos = ",newPos)
        newFood = successorGameState.getFood()
        #print("newFood = ",newFood)
        newGhostStates = successorGameState.getGhostStates()
        #print("newGhostStates = ",newGhostStates)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print("newScaredTimes = ",newScaredTimes)
               

        "*** YOUR CODE HERE ***"
        #print (newFood.asList())
        #exit()
        min_dist_food = -1
        for f in newFood.asList():
            dist_pac_food = util.manhattanDistance(newPos,f)
            if dist_pac_food <= min_dist_food or min_dist_food == -1:
                min_dist_food = dist_pac_food
        
        dist_pac_ghost = 1
        closeness_to_ghost = 0
        #print(successorGameState.getGhostPositions())
        for ghost_pos in successorGameState.getGhostPositions():
            dist = util.manhattanDistance(newPos,ghost_pos)
            dist_pac_ghost = dist_pac_ghost + 1
            if dist <= 1:
                closeness_to_ghost = closeness_to_ghost + 1

        val = successorGameState.getScore()
        val_1 = val + (1/float(min_dist_food)) - (1/float(dist_pac_ghost)) - closeness_to_ghost
        
       
		
		
		
        return val_1

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
        """
        "*** YOUR CODE HERE ***"

        def minimax(agent, depth, gameState):
            if gameState.isLose(): #return score if Pacman Lose
                return self.evaluationFunction(gameState)
            elif gameState.isWin(): #return Score if Pacman Win
                return self.evaluationFunction(gameState)
            elif depth == self.depth:#return Score if depth is reached
				return self.evaluationFunction(gameState)
            if agent == 0:  # Pacman is the maximising agent
                return max(minimax(1, depth, gameState.generateSuccessor(agent, this_action)) for this_action in gameState.getLegalActions(agent))
            else:  # Ghosts are the minimizing agents
                new_Agent = agent + 1
                if gameState.getNumAgents() == new_Agent:
                    new_Agent = 0
                if new_Agent == 0:
                    depth += 1
                return min(minimax(new_Agent, depth, gameState.generateSuccessor(agent, this_action)) for this_action in gameState.getLegalActions(agent))

        
        x= float("-inf")
        max1 = x
        action = Directions.STOP
        legal_actions = [act for act in gameState.getLegalActions(0)]
		#print(legal_actions)
        for legal_action in legal_actions:
            utility = minimax(1, 0, gameState.generateSuccessor(0, legal_action))
            if utility > max1 or max1 == x:
                max1 = utility
                action = legal_action

        return action

        
			 
                 
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimise(agent, depth, game_state, a, b): 
            v = float("inf")
            new_agent = agent + 1 
            if game_state.getNumAgents() == new_agent:
                new_agent = 0
            if new_agent == 0:
                depth += 1
            legal_actions = game_state.getLegalActions(agent)			
            for legal_action in legal_actions:
                v = min(v, prune(new_agent, depth, game_state.generateSuccessor(agent, legal_action), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v
		
        def maximise(agent, depth, game_state, a, b):
            v = float("-inf")
            legal_actions = game_state.getLegalActions(agent)	
            for legal_action in legal_actions:
                v = max(v, prune(1, depth, game_state.generateSuccessor(agent, legal_action), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v
            
        def prune(agent, depth, game_state, a, b):
            if game_state.isLose(): 
                return self.evaluationFunction(game_state)
            elif game_state.isWin():
                return self.evaluationFunction(game_state)
            elif depth == self.depth:
                return self.evaluationFunction(game_state)
            if agent == 0:  # Pacman: maximising agent
                return maximise(agent, depth, game_state, a, b)
            else:  # Ghosts: minimizing agent
                return minimise(agent, depth, game_state, a, b)

       
        x = float("-inf")
        utility = x
        action = Directions.STOP
        y = float("-inf")
        a = y
        z = float("inf")
        b = z
        legal_actions = [act for act in gameState.getLegalActions(0)]
        for legal_action in legal_actions:
            ghost_val = prune(1, 0, gameState.generateSuccessor(0, legal_action), a, b)
            if ghost_val > utility:
                utility = ghost_val
                action = legal_action
            if utility > b:
                return utility
            a = max(a, utility)
        return action
        
        #util.raiseNotDefined()

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
        def expectimax(agent, depth, gameState):
            if gameState.isLose():  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(gameState)
            elif gameState.isWin():
                return self.evaluationFunction(gameState)
            elif depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:  # maximizing for pacman
                legal_actions = [act for act in gameState.getLegalActions(agent)]
                return max(expectimax(1, depth, gameState.generateSuccessor(agent, legal_action)) for legal_action in legal_actions)
            else:  # performing expectimax action for ghosts/chance nodes.
                new_Agent = agent + 1  # calculate the next agent and increase depth accordingly.
                if gameState.getNumAgents() == new_Agent:
                    new_Agent = 0
                if new_Agent == 0:
                    depth += 1
                legal_actions = [act for act in gameState.getLegalActions(agent)]
                return sum(expectimax(new_Agent, depth, gameState.generateSuccessor(agent, legal_action)) for legal_action in legal_actions) / float(len(legal_actions))

        
        x = float("-inf")
        max1 = x
        action = Directions.STOP
        legal_actions = [act for act in gameState.getLegalActions(0)]
        for legal_action in legal_actions:
            utility = expectimax(1, 0, gameState.generateSuccessor(0, legal_action))
            if utility > max1 or max1 == x:
                max1 = utility
                action = legal_action

        return action 
        #util.raiseNotDefined()
        

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

