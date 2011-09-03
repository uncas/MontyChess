class Move:
    
    def __init__(self, origin, destination):
        self.Origin = origin
        self.Destination = destination

    def __repr__(self):
        return "Move from " + str(self.Origin) + " to " + str(self.Destination) + "."

    def __eq__(self, other):
        return self.Origin == other.Origin and self.Destination == other.Destination
