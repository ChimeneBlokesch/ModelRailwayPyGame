from objparser import Object3D
from position import Position


class BasisObject:
    def __init__(self, obj_name, folder, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0, mtl_images={}):
        self.obj_name = obj_name
        self.folder = folder
        self.mtl_images = mtl_images
        self.object = self.create_object()

        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)

    def create_object(self):
        model = Object3D(self.folder, self.obj_name)

        if self.mtl_images:
            model.change_img(self.mtl_images, self.folder)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        self.object.render(self.pos)
