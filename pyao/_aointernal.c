#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ao/ao.h>
#define BUF_SIZE 4096

// AO Device Descriptor
ao_device** aodd = NULL;

static PyObject* pyao_init(PyObject* self) {
    ao_initialize();
    Py_RETURN_NONE;
}

static PyObject* pyao_shutdown(PyObject* self) {
    ao_shutdown();
    Py_RETURN_NONE;
}

static PyObject* pyao_default_driver_id(PyObject* self) {
    int drvid = ao_default_driver_id();
    return Py_BuildValue("i", drvid);
}

static PyObject* pyao_open_live(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid;
    ao_device* device;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));
    PyObject pyfmt;

    static char* argsname[] = {"default_driver", "format", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "id:pyao_open_live", argsname,
                &drvid, &pyfmt
                ))
        return NULL;

    // pick objects from dict
    PyObject* bits = PyDict_GetItemString(&pyfmt, "bits");
    PyObject* channels = PyDict_GetItemString(&pyfmt, "channels");
    PyObject* rate = PyDict_GetItemString(&pyfmt, "bitrate");
    PyObject* byte_format = PyDict_GetItemString(&pyfmt, "byte_format");
    // PyObject* matrix = PyDict_GetItemString(&pyfmt, "matrix");

    aofmt.bits = _PyLong_AsInt(bits);
    aofmt.channels = _PyLong_AsInt(channels);
    aofmt.rate = _PyLong_AsInt(rate);
    aofmt.byte_format = _PyLong_AsInt(byte_format);
    // aofmt.matrix = PyUnicode_AsString(matrix);

    device = ao_open_live(drvid, &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }
    int index = sizeof(aodd);
    aodd = (ao_device**)realloc(aodd, sizeof(ao_device*) * (index + 1));
    return Py_BuildValue("i", index);
}

static PyObject* pyao_close(PyObject* self, PyObject* args) {
    int descriptor;
    if (!PyArg_ParseTuple(args, "i:pyao_close", &descriptor))
        return NULL;
    int code = ao_close(aodd[descriptor]);
    return Py_BuildValue("i", code);
}

static PyMethodDef _methods[] = {
    {"pyao_init",               (PyCFunction)pyao_init,                 METH_NOARGS},
    {"pyao_shutdown",           (PyCFunction)pyao_shutdown,             METH_NOARGS},
    {"pyao_default_driver_id",  (PyCFunction)pyao_default_driver_id,    METH_NOARGS},
    {"pyao_open_live",          (PyCFunction)pyao_open_live,            METH_VARARGS | METH_KEYWORDS},
    {"pyao_close",              (PyCFunction)pyao_close,                METH_VARARGS},
    {NULL, NULL}
};

static struct PyModuleDef _module = {
    PyModuleDef_HEAD_INIT,
    "_aointernal",
    "Basic interface of libao for Python",
    -1,
    _methods
};

PyMODINIT_FUNC PyInit__aointernal() {
    PyObject *mod;
    mod = PyModule_Create(&_module);
    PyModule_AddIntMacro(mod, AO_FMT_LITTLE);
    PyModule_AddIntMacro(mod, AO_FMT_BIG);
    PyModule_AddIntMacro(mod, AO_FMT_NATIVE);
    return mod;
}
