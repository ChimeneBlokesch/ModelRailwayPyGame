import os

FILENAME = "database_trains.txt"
PATH = os.path.join("sprites", "trains")


class TrainFormat:
    def __init__(self, name: str, amount_imgs: int, img_ext: int,
                 max_speed: int, acceleration: int):
        self.folder = name
        self.amount_imgs = amount_imgs
        self.img_ext = img_ext
        self.max_speed = max_speed
        self.acceleration = acceleration

    @property
    def degrees_step(self):
        """
        For each image in the folder, its next image is the rotated version
        of the current one. The difference in degrees is returned.
        """
        return 360 / self.amount_imgs

    def get_sprite_file_path(self, degrees: float):
        idx = int(degrees / self.degrees_step)
        return os.path.join(PATH, self.folder, str(idx) + self.img_ext)


class Database:
    def __init__(self):
        self.trains: list[TrainFormat] = self.read_file()

    def read_file(self):
        data = []

        with open(FILENAME) as f:
            for line in f.readlines()[1:]:
                if line.startswith("#"):
                    continue

                line = line.split()

                i = 0
                name = line[i]
                i += 1
                amount_imgs = int(line[i])
                i += 1
                img_ext = line[i]
                i += 1
                max_speed = int(line[i])
                i += 1
                acceleration = int(line[i])

                data.append(TrainFormat(name,
                                        amount_imgs,
                                        img_ext,
                                        max_speed,
                                        acceleration))

        return data

    def get_train(self, filename: str) -> TrainFormat | None:
        trains = (t for t in self.trains if t.folder == filename)
        return next(trains, None)


# Only for testing:
if __name__ == "__main__":
    db = Database()
