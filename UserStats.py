class UserStats:

    def __init__(self, uname, score, bot):
        self.uname = uname
        self.score = score
        self.bot = bot

    def output(self):
        return "Stats for: {}\nPoints: {}".format(self.uname, self.score)

    def add_score(self, points):
        self.score += points