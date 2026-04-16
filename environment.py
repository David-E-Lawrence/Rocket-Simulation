class Environment:
    def __init__(self, g):
        self.g=g
def Earth():
    return Environment(g=9.81)