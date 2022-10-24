#include <stdio.h>
#define PY_SSIZE_T_CLEAN

#ifndef PYINCDIR
#include <python3.10/Python.h>
#include <python3.10/methodobject.h>
#include <python3.10/moduleobject.h>
#include <python3.10/pyport.h>
#include <python3.10/modsupport.h>
#include <python3.10/object.h>
#include <python3.10/pyerrors.h>
#include <python3.10/pymem.h>
#else
#include <Python.h>
#endif
#include <ao/ao.h>

static ao_device **ao_device_list = NULL;
static ssize_t ao_device_count = 0;

ssize_t add_ao_device(ao_device* dev) {
    if (dev == NULL) return -1;
    ao_device_list = (ao_device**)PyMem_Realloc(ao_device_list, ao_device_count + 1);
    ao_device_list[ao_device_count] = dev;
    return ao_device_count++;
}

static PyObject *pyao_open_live(PyObject* self, PyObject* args, PyObject* kwargs) {
    static char* argsname[] = {"driver", "bits", "rate", "channels", "byte_format", "matrix", NULL};
    int drv = -1;
    ao_sample_format aosf = {};

    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "iiiiis:pyao_open_live", argsname,
        &drv, &aosf.bits, &aosf.rate, &aosf.channels, &aosf.byte_format, &aosf.matrix)) return NULL;

    ao_device* dev = ao_open_live(drv, &aosf, NULL);
    if (dev == NULL) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return Py_BuildValue("i", add_ao_device(dev));
}

static PyObject *pyao_close(PyObject* self, PyObject* args) {
    int dev = -1;
    if (!PyArg_ParseTuple(args, "i:pyao_close", &dev)) return NULL;

    ao_device *device = ao_device_list[dev];
    if (!ao_close(device)) {
        PyErr_SetString(PyExc_OSError, "Cannot close a closed device.");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject *pyao_play(PyObject* self, PyObject* args, PyObject* kwargs) {
    static char *argsname[] = {"device", "data", NULL};
    int dev = -1; char *bytes; Py_ssize_t len = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iy#:pyao_play", argsname, &dev, &bytes, &len)) return NULL;

    ao_device *_dev = ao_device_list[dev];
    return Py_BuildValue("i", ao_play(_dev, bytes, len));
}

static PyMethodDef _methods[] = {
    {
        "pyao_open_live", (PyCFunction)pyao_open_live, METH_VARARGS | METH_KEYWORDS,
        "pyao_open_live(driver, bits, rate, channels, byte_format, matrix)\n--\n\n"
        "Open an audio device for live playback."
    },
    {
        "pyao_close", (PyCFunction)pyao_close, METH_VARARGS,
        "pyao_close(device)\n--\n\n"
        "Close an audio device."
    },
    {
        "pyao_play", (PyCFunction)pyao_play, METH_VARARGS | METH_KEYWORDS,
        "pyao_play(device, data)\n--\n\n"
        "Play data on a live audio device."
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _module = {
    PyModuleDef_HEAD_INIT,
    "_ao_c",
    "Basic interface of libao.",
    -1,
    _methods
};

PyMODINIT_FUNC PyInit__ao_c() {
    PyObject *mod = PyModule_Create(&_module);
    return mod;
}