from BaseAI import BaseAI
import time


class IntelligentAgent(BaseAI):
    startTime = None
    
    def getMove(self, grid):
        self.startTime = time.time()
        depth = 5
        utility = 0
        child = 0

        while time.time() - self.startTime <= 0.12:
            maxChild, maxUtility = self.maximize(grid, float('-inf'), float('inf'), depth)
            if maxUtility > utility and maxChild is not None:
                utility = maxUtility
                child = maxChild

            depth += 1
        return child[0] if child else None
            
    def tile_probability(self, state, alpha, beta, depth):
        if depth == 0 or time.time() - self.startTime > 0.12:
            maxScore = self.heuristics(state)
            return maxScore
            
        return (0.9 * self.minimize(state, alpha, beta, depth - 1, 2)) + (0.1 * self.minimize(state, alpha, beta, depth - 1, 4))
    

    def maximize(self, state, alpha, beta, depth):
        
        if self.terminal_test_max(state) or depth == 0 or time.time() - self.startTime > 0.12:
            maxScore = self.heuristics(state)
            return None, maxScore
        
        maxChild, maxUtility = None, float('-inf')
        
        for child in state.getAvailableMoves():
            utility = self.tile_probability(child[1], alpha, beta, depth - 1)
            
            if utility > maxUtility:
                maxChild, maxUtility = child, utility
                
            if maxUtility >= beta:
                break
            
            if maxUtility > alpha:
                alpha = maxUtility
                
        return maxChild, maxUtility
            
    
    def minimize(self, state, alpha, beta, depth, value):
        
        if self.terminal_test_min(state) or depth == 0 or time.time() - self.startTime > 0.12:
            maxScore = self.heuristics(state)
            return maxScore
        
        minUtility = float('inf')
        
        for cell in state.getAvailableCells():
            chanceOfNumber = state.clone()
            chanceOfNumber.insertTile(cell, value)
            
            notUsed, utility = self.maximize(chanceOfNumber, alpha, beta, depth - 1)
            
            if utility < minUtility:
                minUtility = utility
                
            if minUtility <= alpha:
                break
            
            if minUtility < beta:
                beta = minUtility
        
        return minUtility
    
    
    def terminal_test_max(self, state):
        if len(state.getAvailableMoves()) == 0:
            return True
        
        return False
    
    def terminal_test_min(self, state):
        if len(state.getAvailableCells()) == 0:
            return True
        
        return False
    
    """def board_score(self, child):
        count = 0
        for x in range(child.size):
            for y in range(child.size):
                count += child.map[x][y]

        return count"""
    
    def empty_tiles(self, state):
        count = len(state.getAvailableCells())

        return count
    
    """def possible_merges(self, state):
        count = 0
        x = 0
        y = 0
        while x < 4:
            while y < 3:
                if state.map[x][y] == state.map[x][y+1] and state.map[x][y] != 0:
                    count += state.map[x][y+1]
                    state.map[x][y+1] = 0
                if state.map[y+1][x] == state.map[y][x] and state.map[y][x] != 0:
                    count += state.map[y+1][x]
                    state.map[y+1][x] = 0
                y += 1
            x += 1

        return count
    
    def increasing_tiles(self, state):
        count = 0
        x = 0
        y = 0
        while x < 4:
            while y < 3:
                if state.map[x][y] > state.map[x][y+1]:
                    count += state.map[x][y]
                if state.map[y+1][x] > state.map[x][y]:
                    count += state.map[y+1][x]
                y += 1
            x += 1
        return count"""
            
    
    def snake(self, state):
        
    	gradients = [[4 ** 12, 4 ** 13, 4 ** 14, 4 ** 15],
                    [4 ** 11, 4 ** 10, 4 ** 9, 4 ** 8],
                    [4 ** 4, 4 ** 5, 4 ** 6, 4 ** 7],
                    [4 ** 3, 4 ** 2, 4 ** 1, 4 ** 0]]
    	value = 0
    
    	for x in range(4):
    		for y in range(4):
                 value += state.map[x][y] * gradients[x][y]
    	return value
    
    def heuristics(self, state):

        #score = self.board_score(state)
        empty = self.empty_tiles(state)
        #merges = self.possible_merges(state)
        #increase = self.increasing_tiles(state)
        snake = self.snake(state)
            
        return (empty * 750) + snake
    
    
    
    
    
    