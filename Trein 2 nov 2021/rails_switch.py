class Switch:
    def __init__(self, x, y, direction, speeds):
        self.x = x
        self.y = y
        self.direction = direction  # 1 if direction is right/bottom else -1
        self.speeds = speeds  # first is left/up second is right/bottom
        self.rules = {}

    def switch(self, train_id):
        if train_id not in self.rules:
            return self.speeds[0]

        return self.speeds[self.rules[train_id] == 1 | 0]

    def add_rule(self, train_id, direction):
        direction = 1

        if direction == "u" or direction == "l":
            direction = -1

        self.rules[train_id] = direction
