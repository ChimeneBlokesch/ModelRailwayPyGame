FILENAME = "database_treinen.txt"
PATH = "Treinen/"


class Treinen:
    def __init__(self):
        self.treinen = self.read_file()

    def read_file(self):
        data = []

        with open(FILENAME) as f:
            for line in f.readlines()[1:]:
                if line.startswith("#"):
                    continue

                line = line.split()

                if len(line) != 6:
                    continue

                data.append(TreinFormat(line[0], int(line[1]), int(line[2]),
                                        line[3] == "True", line[4] == "False",
                                        line[5]))

        return data

    def get_trein(self, filename):
        treinen = [t for t in self.treinen if t.filename == filename]

        if not len(treinen):
            return None

        return treinen[0]


class TreinFormat:
    def __init__(self, name: str, max_snelheid: int, versnelling: int,
                 tweede_klas: bool, eerste_klas: bool, type: str):
        self.filename = PATH + name
        self.max_snelheid = max_snelheid
        self.versnelling = versnelling
        self.tweede_klas = tweede_klas
        self.eerste_klas = eerste_klas
        self.type = type


# Only for testing:
if __name__ == "__main__":
    db = Treinen()
