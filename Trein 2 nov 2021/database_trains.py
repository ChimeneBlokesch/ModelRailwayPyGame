FILENAME = "database_trains.txt"
PATH = "trains/"


class TrainFormat:
    def __init__(self, name: str, max_speed: int, acceleration: int,
                 second_class: bool, first_class: bool, type: str):
        self.filename = PATH + name
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.is_second_class = second_class
        self.is_first_class = first_class

        # Sprinter (sp) or Intercity (ic)
        self.type = type


class Trains:
    def __init__(self):
        self.trains: list[TrainFormat] = self.read_file()

    def read_file(self):
        data = []

        with open(FILENAME) as f:
            for line in f.readlines()[1:]:
                if line.startswith("#"):
                    continue

                line = line.split()

                if len(line) != 6:
                    continue

                data.append(TrainFormat(line[0], int(line[1]), int(line[2]),
                                        line[3] == "True", line[4] == "False",
                                        line[5]))

        return data

    def get_train(self, filename) -> TrainFormat | None:
        trains = [t for t in self.trains if t.filename == filename]

        if not len(trains):
            return None

        return trains[0]


# Only for testing:
if __name__ == "__main__":
    db = Trains()
