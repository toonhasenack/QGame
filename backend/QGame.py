import numpy as np

class QGame():
    def __init__(self, size=3, repeat=False):
        self.size = size 
        self.repeat = repeat
        self.grids = [np.zeros([size,size], dtype = int), np.zeros([size,size], dtype = int)]
        self.winner = np.zeros(2, dtype = int)

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
    
    def step(self, player):
        x1 = int(input(f"Player {player}, type the first coordinate of the first game: "))
        y1 = int(input(f"Player {player}, type the second coordinate of the first game: "))
        x2 = int(input(f"Player {player}, type the first coordinate of the second game: "))
        y2 = int(input(f"Player {player}, type the second coordinate of the second game: "))

        proceed = True
        if not self.repeat:
            proceed = (self.grids[0][x1, y1] == 0) and (self.grids[1][y1,y2] == 0)

        if proceed:
            print("Collapsing wave-function...")
            s1, s2 = self.get_sstate()
            self.grids[0][x1,y1] = (player*2-1)*s1
            self.grids[1][x2,y2] = (player*2-1)*s2

            return (player + 1)%2

        else:
            print("Make sure to put in a number 0,1,2 for each coordinate.")
            if not self.repeat:
                print("And pick only non-chosen coordinates!")
            
            return player

    def check(self):
        for i in range(2):
            grid = self.grids[i]
            for j in range(self.size):
                if (np.sum(grid[j,:]) == self.size) or (np.sum(grid[:,j]) == self.size):
                    self.winner[i] = 1
                elif (np.sum(grid[j,:]) == -self.size) or (np.sum(grid[:,j]) == -self.size):
                    self.winner[i] = -1

        if ((self.winner[0] == 1) and (self.winner[1] != -1)) or ((self.winner[0] != -1) and (self.winner[1] == 1)):
            return "Player 1 has won!"
        
        elif ((self.winner[0] == -1) and (self.winner[1] != 1)) or ((self.winner[0] != 1) and (self.winner[1] == -1)):
            return "Player 2 has won!"
        
        elif ((self.winner[0] == 1) and (self.winner[1] == -1)) or ((self.winner[0] == -1) and (self.winner[1] == 1)):
            return "It's a tie!"
        
        else:
            return False

    def run(self):
        won = False
        p = 0
        while not won:
            p = self.step(p)
            won = self.check()
            print(self.grids[0])
            print("\n")
            print(self.grids[1])
        print(won)

if __name__ == '__main__':
    QG = QGame()
    QG.run()
