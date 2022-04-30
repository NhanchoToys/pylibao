#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ao/ao.h>

#define MAX_DEVICE_COUNT 2048

// ao_device descriptor
ao_device* ao_device_list[MAX_DEVICE_COUNT];
int ao_device_count = 0;

// (deprecated) global fast play device
ao_device* ao_fastplay_dev = NULL;
ao_sample_format* fast_fmt = NULL;

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

// add device into device list
int add_ao_device(ao_device *device) {
    if (device == NULL) {
        return -1;
    }
    if (ao_device_count >= MAX_DEVICE_COUNT) {
        return -2;
    }
    ao_device_list[ao_device_count] = device;
    return ao_device_count++;
}

static PyObject* pyao_open_live(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid;
    ao_device* device;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));
    PyObject* pyfmt;

    static char* argsname[] = {"driver", "bits", "chs", "rate", "bfmt", "matrix", NULL};
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
    int d_index = add_ao_device(device);
    return Py_BuildValue("i", d_index);
}

static PyObject* pyao_open_file(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid, ow = 0;
    ao_device* device;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));
    PyObject* pyfmt;
    char* filename;

    static char* argsname[] = {"driver", "filename", "bits", "chs", "rate", "bfmt", "matrix", "overwrite", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "isiiiisi:pyao_open_file", argsname,
                &drvid, &filename, &aofmt.bits, &aofmt.channels, &aofmt.rate, &pyfmt, &aofmt.matrix, &ow
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
    int code = ao_close(device);
    return Py_BuildValue("i", code);
}

static PyObject* pyao_play(PyObject* self, PyObject* args, PyObject* kwargs) {
    int device;
    char* bytes;
    uint_32 size;

    static char* argsname[] = {"device", "data", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iy#:pyao_play", argsname, &device, &bytes, &size))
        return NULL;

    ao_device* _device = ao_device_list[device];
    int code = ao_play(_device, bytes, size);
    return Py_BuildValue("i", code);
}

// (deprecated) initialize fast play device
static PyObject* pyao_fast_play_init(PyObject* self, PyObject* args, PyObject* kwargs) {
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {"bits", "chs", "rate", "bfmt", "matrix", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "iiiis:pyao_fast_play_init", argsname,
                &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format, &aofmt.matrix
                ))
        return NULL;

    fast_fmt = &aofmt;

    ao_fastplay_dev = ao_open_live(ao_default_driver_id(), &aofmt, NULL);
    Py_RETURN_NONE;
}

// (deprecated) close fast play device
static PyObject* pyao_fast_play_close(PyObject* self) {
    ao_close(ao_fastplay_dev);
    Py_RETURN_NONE;
}

// directly play data to fast play device
static PyObject* pyao_fast_play(PyObject* self, PyObject* args, PyObject* kwargs) {
    char* bytes;
    uint_32 size;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {"bits", "chs", "rate", "bfmt", "matrix", "data", NULL};
    if (!PyArg_ParseTupleAndKeywords(
                args, kwargs, "iiiisy#:pyao_fast_play", argsname,
                &aofmt.bits, &aofmt.channels, &aofmt.rate, &aofmt.byte_format, &aofmt.matrix,
                &bytes, &size
                ))
        return NULL;

    ao_device* device = ao_open_live(ao_default_driver_id(), &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }

    int code = ao_play(device, bytes, size);
    ao_close(ao_fastplay_dev);
    return Py_BuildValue("i", 0);
}

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

// fast play sine wave
static PyObject* pyao_fast_play_sine(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid = ao_default_driver_id();
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "freq", "volume", "duration", NULL // sine
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "ddd:pyao_fast_play_sine", argsname,
        &freq, &volume, &duration
    ))
        return NULL;

    aofmt.bits = 16;
    aofmt.channels = 2;
    aofmt.rate = 44100;
    aofmt.byte_format = AO_FMT_LITTLE;

    ao_device* device = ao_open_live(drvid, &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    gen_sine(buf, bufsize, &aofmt, freq, volume, duration);

    int code = ao_play(device, buf, bufsize);
    ao_close(device);
    free(buf);
    return Py_BuildValue("i", code);
}

// fast play square wave
static PyObject* pyao_fast_play_square(PyObject* self, PyObject* args, PyObject* kwargs) {
    int drvid = ao_default_driver_id();
    double freq, volume, duration;
    ao_sample_format aofmt;
    memset(&aofmt, 0, sizeof(aofmt));

    static char* argsname[] = {
        "freq", "volume", "duration", NULL // sine
    };
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "ddd:pyao_fast_play_sine", argsname,
        &freq, &volume, &duration
    ))
        return NULL;

    aofmt.bits = 16;
    aofmt.channels = 2;
    aofmt.rate = 44100;
    aofmt.byte_format = AO_FMT_LITTLE;

    ao_device* device = ao_open_live(ao_default_driver_id(), &aofmt, NULL);
    if (device == NULL) {
        PyErr_SetString(PyExc_OSError, "Unable to open an audio device");
        return NULL;
    }

    uint32_t bufsize = aofmt.bits / 8 * aofmt.channels * aofmt.rate * duration;
    char* buf = (char*)calloc(bufsize, sizeof(char));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate memory");
        return NULL;
    }

    for (uint32_t i = 0; i < (uint32_t)(aofmt.rate * duration); i++) {
        double t = (double)i / aofmt.rate;
        int sample = (int)(volume * 32768 * (sin(2 * M_PI * freq * t) > 0 ? 1 : -1));
        if (aofmt.byte_format == AO_FMT_LITTLE) {
            buf[i * aofmt.channels * aofmt.bits / 8] = sample & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 1] = (sample >> 8) & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 2] = sample & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 3] = (sample >> 8) & 0xFF;
        } else if (aofmt.byte_format == AO_FMT_BIG) {
            buf[i * aofmt.channels * aofmt.bits / 8] = (sample >> 8) & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 1] = sample & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 2] = (sample >> 8) & 0xFF;
            buf[i * aofmt.channels * aofmt.bits / 8 + 3] = sample & 0xFF;
        }
    }

    int code = ao_play(device, buf, bufsize);
    free(buf);
    ao_close(device);
    return Py_BuildValue("i", code);
}

static PyMethodDef _methods[] = {
    {"pyao_init",               (PyCFunction)pyao_init,                 METH_NOARGS,                    "pyao_init()\n--\n\nInitialize the audio library."},
    {"pyao_shutdown",           (PyCFunction)pyao_shutdown,             METH_NOARGS,                    "pyao_shutdown()\n--\n\nShutdown the audio library."},
    {"pyao_default_driver_id",  (PyCFunction)pyao_default_driver_id,    METH_NOARGS,                    "pyao_default_driver_id()\n--\n\nGet the default audio driver ID."},
    {"pyao_open_live",          (PyCFunction)pyao_open_live,            METH_VARARGS | METH_KEYWORDS,   "pyao_open_live(driver, bits, chs, rate, bfmt, matrix)\n--\n\nOpen an audio device for live playback."},
    {"pyao_open_file",          (PyCFunction)pyao_open_file,            METH_VARARGS | METH_KEYWORDS,   "pyao_open_file(driver, filename, bits, chs, rate, bfmt, matrix, overwrite)\n--\n\nOpen an audio device for file playback."},
    {"pyao_close",              (PyCFunction)pyao_close,                METH_VARARGS,                   "pyao_close(device)\n--\n\nClose an audio device."},
    {"pyao_play",               (PyCFunction)pyao_play,                 METH_VARARGS | METH_KEYWORDS,   "pyao_play(device, data)\n--\n\nPlay a buffer on an audio device."},
    {"pyao_fast_play_init",     (PyCFunction)pyao_fast_play_init,       METH_VARARGS | METH_KEYWORDS,   "pyao_fast_play_init(bits, chs, rate, bfmt, matrix)\n--\n\nInitialize a fast playback device."},
    {"pyao_fast_play",          (PyCFunction)pyao_fast_play,            METH_VARARGS | METH_KEYWORDS,   "pyao_fast_play(data)\n--\n\nPlay a buffer on a fast playback device."},
    {"pyao_fast_play_sine",     (PyCFunction)pyao_fast_play_sine,       METH_VARARGS | METH_KEYWORDS,   "pyao_fast_play_sine(freq, volume, duration)\n--\n\nPlay a sine wave on a fast playback device."},
    {"pyao_fast_play_square",   (PyCFunction)pyao_fast_play_square,     METH_VARARGS | METH_KEYWORDS,   "pyao_fast_play_square(freq, volume, duration)\n--\n\nPlay a square wave on a fast playback device."},
    {"pyao_fast_play_close",    (PyCFunction)pyao_fast_play_close,      METH_VARARGS,                   "pyao_fast_play_close(device)\n--\n\nClose a fast playback device."},
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
