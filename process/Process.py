from pygame import Surface


# It's an interface :)
# Formally it is more complicated so we use this
class Process:
    def processEvents(self, events: list):
        pass

    def update(self, delta: float):
        pass

    def draw(self, dst: Surface):
        pass
