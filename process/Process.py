from pygame import Surface


# It's an interface :)
# Formally it is more complicated so we use this
class Process:
    def processEvents(self, events: list):
        pass

    def update(self):
        pass

    def draw(self, screen: Surface):
        pass
