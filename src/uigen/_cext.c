/**
 * uigen C extension — fast HTML escaping
 *
 * This module provides C-accelerated HTML entity escaping.
 *
 * Build with: python setup.py build_ext --inplace
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
#include <stdlib.h>

/**
 * Fast HTML entity escaping
 */
static PyObject* escape_html(PyObject* self, PyObject* args) {
    const char* input;
    Py_ssize_t input_len;

    if (!PyArg_ParseTuple(args, "s#", &input, &input_len)) {
        return NULL;
    }

    /* Allocate output buffer (worst case: every char needs escaping) */
    char* output = (char*)malloc(input_len * 7 + 1);
    if (!output) {
        return PyErr_NoMemory();
    }

    char* out = output;
    for (Py_ssize_t i = 0; i < input_len; i++) {
        char c = input[i];
        switch (c) {
            case '&':  memcpy(out, "&amp;", 5);  out += 5; break;
            case '<':  memcpy(out, "&lt;", 4);   out += 4; break;
            case '>':  memcpy(out, "&gt;", 4);   out += 4; break;
            case '"':  memcpy(out, "&quot;", 6); out += 6; break;
            case '\'': memcpy(out, "&#39;", 5);  out += 5; break;
            default:   *out++ = c; break;
        }
    }
    *out = '\0';

    PyObject* result = PyUnicode_FromString(output);
    free(output);
    return result;
}

/**
 * Module method definitions
 */
static PyMethodDef uigen_methods[] = {
    {
        "escape_html",
        escape_html,
        METH_VARARGS,
        "Escape HTML special characters"
    },
    {NULL, NULL, 0, NULL}
};

/**
 * Module definition
 */
static struct PyModuleDef uigen_module = {
    PyModuleDef_HEAD_INIT,
    "uigen._cext",
    "uigen C extension for fast HTML escaping",
    -1,
    uigen_methods
};

/**
 * Module initialization
 */
PyMODINIT_FUNC PyInit__cext(void) {
    return PyModule_Create(&uigen_module);
}
