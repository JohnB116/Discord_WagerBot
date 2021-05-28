class UserStats:

    def __init__(self, uname, score):
        self.uname = uname
        self.score = score

    def output(self):
        return "Stats for: {}\nPoints: {}".format(self.uname, self.score)

