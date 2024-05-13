class Player:
    def __init__(self, color):
        self.color = color
        self.score = 30

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
