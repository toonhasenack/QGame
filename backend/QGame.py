import numpy as np

class QGame():
    def __init__(self, size=3, repeat=False):
        self.size = size 
        self.repeat = repeat
        self.grids = [np.zeros([size,size], dtype = int), np.zeros([size,size], dtype = int)]
        self.steps = 0
        self.player = 0
        self.winner = False

    def get_qstate(self):
        '''
        Function to handle wave-function collapse with external qubits
        Returns either -1 or +1
        '''
        pass

    def get_sstate(self):
        '''
        Function to simulate wave-function collapse with conventional bits.
        Returns either -1 or +1
        '''
        val = np.random.binomial(1, 0.5)
        state1 = 2*val - 1
        state2 = -state1
        return state1, state2
    
    def step(self, coords):
        x1, x2 = coords[0]
        y1, y2 = coords[1]

        proceed = all(coord >= 0 for coord in coords[0]) and all(coord <= self.size - 1 for coord in coords[0])\
            and all(coord >= 0 for coord in coords[1]) and all(coord <= self.size - 1 for coord in coords[1])
        
        if not self.repeat and proceed:
            proceed = (self.grids[0][x1, y1] == 0) and (self.grids[1][y1,y2] == 0)

        if proceed:
            s1, s2 = self.get_sstate()
            self.grids[0][x1,y1] = (self.player*2-1)*s1
            self.grids[1][x2,y2] = (self.player*2-1)*s2
            self.steps += 1
            return True
        
        else:
            return False

    def check(self):
        winner = np.zeros(2)
        for i in range(2):
            grid = self.grids[i]
            for j in range(self.size):
                if (np.sum(grid[j,:]) == self.size) or (np.sum(grid[:,j]) == self.size):
                    winner[i] = 1
                elif (np.sum(grid[j,:]) == -self.size) or (np.sum(grid[:,j]) == -self.size):
                    winner[i] = -1

        if ((self.winner[0] == 1) and (self.winner[1] != -1)) or ((self.winner[0] != -1) and (self.winner[1] == 1)):
            self.winner =  "Player 1"
        
        elif ((self.winner[0] == -1) and (self.winner[1] != 1)) or ((self.winner[0] != 1) and (self.winner[1] == -1)):
            self.winner =  "Player 2"
        
        elif ((self.winner[0] == 1) and (self.winner[1] == -1)) or ((self.winner[0] == -1) and (self.winner[1] == 1)) or (self.steps == self.size**2):
            self.winner =  "Tie"
        
        else:
            pass
