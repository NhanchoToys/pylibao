#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ao/ao.h>

// ao_device descriptor
static ao_device** ao_device_list = NULL;
static int ao_device_count = 0;

// initialize
static PyObject* pyao_init(PyObject* self) {
    ao_initialize();
    Py_RETURN_NONE;
}

// shutdown
static PyObject* pyao_shutdown(PyObject* self) {
    ao_shutdown();
    Py_RETURN_NONE;
}

// get default driver ID
static PyObject* pyao_default_driver_id(PyObject* self) {
    int drvid = ao_default_driver_id();
    return Py_BuildValue("i", drvid);
}

// wave generating
void gen_sine(char* buf, uint32_t bufsize, ao_sample_format* aofmt, double freq, double volume, double duration) {
    for (uint32_t i = 0; i < (uint32_t)(aofmt->rate * duration); i++) {
        double t = (double)i / aofmt->rate;
        int sample = (int)(volume * 32768 * sin(2 * M_PI * freq * t));
        if (aofmt->byte_format == AO_FMT_LITTLE) {
            buf[i * aofmt->channels * aofmt->bits / 8] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = (sample >> 8) & 0xFF;
        } else if (aofmt->byte_format == AO_FMT_BIG) {
            buf[i * aofmt->channels * aofmt->bits / 8] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = sample & 0xFF;
        }
    }
}

void gen_square(char* buf, uint32_t bufsize, ao_sample_format* aofmt, double freq, double volume, double duration) {
    for (uint32_t i = 0; i < (uint32_t)(aofmt->rate * duration); i++) {
        double t = (double)i / aofmt->rate;
        int sample = (int)(volume * 32768 * (sin(2 * M_PI * freq * t) > 0));
        if (aofmt->byte_format == AO_FMT_LITTLE) {
            buf[i * aofmt->channels * aofmt->bits / 8] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = (sample >> 8) & 0xFF;
        } else if (aofmt->byte_format == AO_FMT_BIG) {
            buf[i * aofmt->channels * aofmt->bits / 8] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = sample & 0xFF;
        }
    }
}

void gen_triangle(char* buf, uint32_t bufsize, ao_sample_format* aofmt, double freq, double volume, double duration) {
    for (uint32_t i = 0; i < (uint32_t)(aofmt->rate * duration); i++) {
        double t = (double)i / aofmt->rate;
        int sample = (int)(volume * 32768 * (2 * fabs(sin(M_PI * freq * t)) - 1));
        if (aofmt->byte_format == AO_FMT_LITTLE) {
            buf[i * aofmt->channels * aofmt->bits / 8] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = (sample >> 8) & 0xFF;
        } else if (aofmt->byte_format == AO_FMT_BIG) {
            buf[i * aofmt->channels * aofmt->bits / 8] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = sample & 0xFF;
        }
    }
}

void gen_saw(char* buf, uint32_t bufsize, ao_sample_format* aofmt, double freq, double volume, double duration) {
    for (uint32_t i = 0; i < (uint32_t)(aofmt->rate * duration); i++) {
        double t = (double)i / aofmt->rate;
        int sample = (int)(volume * 32768 * (t / duration - sin(2 * M_PI * freq * t) / (2 * M_PI * freq * t)));
        if (aofmt->byte_format == AO_FMT_LITTLE) {
            buf[i * aofmt->channels * aofmt->bits / 8] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = (sample >> 8) & 0xFF;
        } else if (aofmt->byte_format == AO_FMT_BIG) {
            buf[i * aofmt->channels * aofmt->bits / 8] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 1] = sample & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 2] = (sample >> 8) & 0xFF;
            buf[i * aofmt->channels * aofmt->bits / 8 + 3] = sample & 0xFF;
        }
    }
}

// add device into device list
int add_ao_device(ao_device *device) {
    if (device == NULL) {
        return -1;
    }
    ao_device_list = (ao_device**)realloc(ao_device_list, sizeof(ao_device*) * (ao_device_count + 1));
    ao_device_list[ao_device_count] = device;
    return ao_device_count++;
}

static PyObject* pyao_open_live(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid;
    ao_device* device;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {"driver", "bits", "chs", "rate", "bfmt", "matrix", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "iiiiis:pyao_open_live", argsname,
                &drvid, &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format, &aofmt.matrix
                ))
        return NULL;

    device = ao_open_live(drvid, &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }
    int d_index = add_ao_device(device);
    return Py_BuildValue("i", d_index);
}

static PyObject* pyao_open_file(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid, ow = 0;
    static ao_device* device;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));
    char* filename;

    static char* argsname[] = {"driver", "filename", "bits", "chs", "rate", "bfmt", "matrix", "overwrite", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "isiiiisi:pyao_open_file", argsname,
                &drvid, &filename, &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format, &aofmt.matrix, &ow
                ))
        return NULL;

    device = ao_open_file(drvid, filename, ow, &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }
    int d_index = add_ao_device(device);
    return Py_BuildValue("i", d_index);
}

static PyObject* pyao_close(PyObject* self, PyObject* args) {
    int d_index;
    if (!PyArg_ParseTuple(args, "i:pyao_close", &d_index))
        return NULL;

    ao_device* device = ao_device_list[d_index];
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Cannot close a closed device");
        return NULL;
    }
    int code = ao_close(device);
    return Py_BuildValue("i", code);
}

static PyObject* pyao_play(PyObject* self, PyObject* args, PyObject* kwargs) {
    int device;
    char* bytes;
    Py_ssize_t len;

    static char* argsname[] = {"device", "data", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iy#:pyao_play", argsname, &device, &bytes, &len))
        return NULL;

    ao_device* _device = ao_device_list[device];
    int code = ao_play(_device, bytes, len);
    return Py_BuildValue("i", code);
}

// generate sine wave
static PyObject* pyao_gen_sine(PyObject* self, PyObject* args, PyObject* kwargs) {
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "bits", "chs", "rate", "bfmt",
        "freq", "volume", "duration", NULL // sine
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "iiiiddd:pyao_fast_play_sine", argsname,
        &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format,
        &freq, &volume, &duration
    ))
        return NULL;

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    gen_sine(buf, bufsize, &aofmt, freq, volume, duration);

    return Py_BuildValue("y#", buf, (Py_ssize_t)bufsize);
}

// generate square wave
static PyObject* pyao_gen_square(PyObject* self, PyObject* args, PyObject* kwargs) {
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "bits", "chs", "rate", "bfmt",
        "freq", "volume", "duration", NULL // square
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "iiiiddd:pyao_fast_play_square", argsname,
        &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format,
        &freq, &volume, &duration
    ))
        return NULL;

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    gen_square(buf, bufsize, &aofmt, freq, volume, duration);

    return Py_BuildValue("y#", buf, (Py_ssize_t)bufsize);
}

// generate triangle wave
static PyObject* pyao_gen_triangle(PyObject* self, PyObject* args, PyObject* kwargs) {
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "bits", "chs", "rate", "bfmt",
        "freq", "volume", "duration", NULL // triangle
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "iiiiddd:pyao_fast_play_triangle", argsname,
        &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format,
        &freq, &volume, &duration
    ))
        return NULL;

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    gen_triangle(buf, bufsize, &aofmt, freq, volume, duration);

    return Py_BuildValue("y#", buf, (Py_ssize_t)bufsize);
}

// generate sawtooth wave
PyObject* pyao_gen_sawtooth(PyObject* self, PyObject* args, PyObject* kwargs) {
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "bits", "chs", "rate", "bfmt",
        "freq", "volume", "duration", NULL // sawtooth
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "iiiiddd:pyao_fast_play_sawtooth", argsname,
        &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format,
        &freq, &volume, &duration
    ))
        return NULL;

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    gen_saw(buf, bufsize, &aofmt, freq, volume, duration);

    return Py_BuildValue("y#", buf, (Py_ssize_t)bufsize);
}

static PyMethodDef _methods[] = {
    {"pyao_init",               (PyCFunction)pyao_init,                 METH_NOARGS,                    "pyao_init()\n--\n\nInitialize the audio library."},
    {"pyao_shutdown",           (PyCFunction)pyao_shutdown,             METH_NOARGS,                    "pyao_shutdown()\n--\n\nShutdown the audio library."},
    {"pyao_default_driver_id",  (PyCFunction)pyao_default_driver_id,    METH_NOARGS,                    "pyao_default_driver_id()\n--\n\nGet the default audio driver ID."},
    {"pyao_open_live",          (PyCFunction)pyao_open_live,            METH_VARARGS | METH_KEYWORDS,   "pyao_open_live(driver, bits, chs, rate, bfmt, matrix)\n--\n\nOpen an audio device for live playback."},
    {"pyao_open_file",          (PyCFunction)pyao_open_file,            METH_VARARGS | METH_KEYWORDS,   "pyao_open_file(driver, filename, bits, chs, rate, bfmt, matrix, overwrite)\n--\n\nOpen an audio device for file playback."},
    {"pyao_close",              (PyCFunction)pyao_close,                METH_VARARGS,                   "pyao_close(device)\n--\n\nClose an audio device."},
    {"pyao_play",               (PyCFunction)pyao_play,                 METH_VARARGS | METH_KEYWORDS,   "pyao_play(device, data)\n--\n\nPlay a buffer on an audio device."},
    {"pyao_gen_sine",           (PyCFunction)pyao_gen_sine,             METH_VARARGS | METH_KEYWORDS,   "pyao_gen_sine(bits, chs, rate, bfmt, freq, volume, duration)\n--\n\nGenerate a sine wave."},
    {"pyao_gen_square",         (PyCFunction)pyao_gen_square,           METH_VARARGS | METH_KEYWORDS,   "pyao_gen_square(bits, chs, rate, bfmt, freq, volume, duration)\n--\n\nGenerate a square wave."},
    {"pyao_gen_triangle",       (PyCFunction)pyao_gen_triangle,         METH_VARARGS | METH_KEYWORDS,   "pyao_gen_triangle(bits, chs, rate, bfmt, freq, volume, duration)\n--\n\nGenerate a triangle wave."},
    {"pyao_gen_sawtooth",       (PyCFunction)pyao_gen_sawtooth,         METH_VARARGS | METH_KEYWORDS,   "pyao_gen_sawtooth(bits, chs, rate, bfmt, freq, volume, duration)\n--\n\nGenerate a sawtooth wave."},
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
