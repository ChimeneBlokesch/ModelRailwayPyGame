#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

// Include GLEW. Always include it before gl.h and glfw3.h
#include <GL/glew.h>

// Handles keyboard and window
#include <GLFW/glfw3.h>

// 3D mathematics
#include <glm/glm.hpp>



GLFWwindow* window;
bool is_running = false;


static PyObject *method_loop_begin(PyObject *self) {
    if (!is_running) {
        return Py_BuildValue("i", 0);
    }

    // Clear the screen. It's not mentioned before Tutorial 02, but it can cause flickering, so it's there nonetheless.
    glClear( GL_COLOR_BUFFER_BIT );

    if (!(glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
        glfwWindowShouldClose(window) == 0)) {
           is_running = false;
       }

    return Py_BuildValue("i", 1);
}

static PyObject *method_loop_draw(PyObject *self) {
    if (!is_running) {
        Py_RETURN_NONE;
    }
    // Draw nothing, see you in tutorial 2 !
    Py_RETURN_NONE;
}

static PyObject *method_loop_end(PyObject *self) {
    if (!is_running) {
        Py_RETURN_NONE;
    }

    // Swap buffers
    glfwSwapBuffers(window);
    glfwPollEvents();
    Py_RETURN_NONE;
}

static PyObject *method_init(PyObject *self) {
    // Initialise GLFW
    glewExperimental = true; // Needed for core profile

    if( !glfwInit() ) {
        fprintf( stderr, "Failed to initialize GLFW\n" );
        return Py_BuildValue("i", -1);
    }

    glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // We want OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We don't want the old OpenGL

    // Open a window and create its OpenGL context
    // GLFWwindow* window; // (In the accompanying source code, this variable is global for simplicity)
    window = glfwCreateWindow( 1024, 768, "Tutorial 01", NULL, NULL);

    if( window == NULL ) {
        fprintf( stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n" );
        glfwTerminate();
        return Py_BuildValue("i", -1);
    }

    glfwMakeContextCurrent(window); // Initialize GLEW
    glewExperimental=true; // Needed in core profile

    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return Py_BuildValue("i", -1);
    }

    // Ensure we can capture the escape key being pressed below
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
    is_running = true;
    Py_RETURN_NONE;
}


static PyMethodDef game_methods[] = {
   { "init", (PyCFunction)method_init, METH_NOARGS, NULL },
   { "loop_begin", (PyCFunction)method_loop_begin, METH_NOARGS, NULL },
   { "loop_draw", (PyCFunction)method_loop_draw, METH_NOARGS, NULL },
   { "loop_end", (PyCFunction)method_loop_end, METH_NOARGS, NULL },

   { NULL, NULL, 0, NULL }
};

static struct PyModuleDef game_module = {
    PyModuleDef_HEAD_INIT,
    "game",
    "OpenGL in C for Python",
    -1,
    game_methods
};



PyMODINIT_FUNC PyInit_game(void) {
    return PyModule_Create(&game_module);
}
