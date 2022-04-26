#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ao/ao.h>
#define BUF_SIZE 4096
#define AO_DEVICE_SIZE 84

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
    PyObject* pyfmt;

    static char* argsname[] = {"default_driver", "bits", "chs", "rate", "bfmt", "matrix", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "iiiiis:pyao_open_live", argsname,
                &drvid, &aofmt.bits, &aofmt.channels, &aofmt.rate, &pyfmt, &aofmt.matrix
                ))
        return NULL;

    device = ao_open_live(drvid, &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }
    return Py_BuildValue("y#", (char*)(device), AO_DEVICE_SIZE);
}

static PyObject* pyao_close(PyObject* self, PyObject* args) {
    PyObject* bytes;
    if (!PyArg_ParseTuple(args, "O:pyao_close", bytes))
        return NULL;

    ao_device* device = (ao_device*)malloc(AO_DEVICE_SIZE);
    memcpy(device, PyBytes_AsString(bytes), AO_DEVICE_SIZE);
    int code = ao_close(device);
    return Py_BuildValue("i", code);
}

static PyObject* pyao_play(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* device, bytes;
    uint_32 size;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO#:pyao_play", device, bytes, &size))
        return NULL;

    ao_device* _device = (ao_device*)malloc(AO_DEVICE_SIZE);
    memcpy(_device, PyBytes_AsString(device), AO_DEVICE_SIZE);
    int code = ao_play(_device, PyBytes_AsString(bytes), BUF_SIZE);
    return Py_BuildValue("i", code);
}

static PyMethodDef _methods[] = {
    {"pyao_init",               (PyCFunction)pyao_init,                 METH_NOARGS,                    "Initialize the audio library."},
    {"pyao_shutdown",           (PyCFunction)pyao_shutdown,             METH_NOARGS,                    "Shutdown the audio library."},
    {"pyao_default_driver_id",  (PyCFunction)pyao_default_driver_id,    METH_NOARGS,                    "Get the default audio driver ID."},
    {"pyao_open_live",          (PyCFunction)pyao_open_live,            METH_VARARGS | METH_KEYWORDS,   "Open an audio device for live playback."},
    {"pyao_close",              (PyCFunction)pyao_close,                METH_VARARGS,                   "Close an audio device."},
    {"pyao_play",               (PyCFunction)pyao_play,                 METH_VARARGS | METH_KEYWORDS,   "Play a buffer on an audio device."},
    {NULL,                      NULL,                                   0,                              NULL}
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
