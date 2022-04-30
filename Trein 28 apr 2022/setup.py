import numpy as np
from distutils.core import setup, Extension
import pkgconfig


includes = ["src/pyglui/cygl/", ".", np.get_include()]
glew_binaries = []
lib_dir = []
link_args = []
fontstash_compile_args = [
    "-D FONTSTASH_IMPLEMENTATION",
    "-D GLFONTSTASH_IMPLEMENTATION",
]


pkgconfig_glew = pkgconfig.parse("glew")
pkgconfig_glfw3 = pkgconfig.parse("glfw3")
pkgconfig_gl = pkgconfig.parse("gl")

includes += pkgconfig_glew["include_dirs"]
includes += pkgconfig_glfw3["include_dirs"]
includes += pkgconfig_gl["include_dirs"]

lib_dir += pkgconfig_glew["library_dirs"]
lib_dir += pkgconfig_glfw3["library_dirs"]
lib_dir += pkgconfig_gl["library_dirs"]

libs = pkgconfig_glew["libraries"]
libs += pkgconfig_glfw3["libraries"]
libs += pkgconfig_gl["libraries"]


extra_compile_args = ["-Wno-strict-aliasing", "-O2"]

print("include_dirs", includes)
print("libraries", libs)
print("library_dirs", lib_dir)
print("extra_link_args", link_args)
ex = Extension(
    name="game",
    sources=["game.cpp"],
    include_dirs=includes,
    libraries=libs,
    library_dirs=lib_dir,
    extra_link_args=link_args,
    extra_compile_args=extra_compile_args,
    language="c++",
    define_macros=[("GL_SILENCE_DEPRECATION", "1")],
)

setup(name="game", ext_modules=[ex])
