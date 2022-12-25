#include "pymatrix.h"
#include "matrix.h"

extern "C" {

PyObject *PyMatrix_Create()
{
    PyObject *argsList = PyTuple_New(0);

    PyObject *obj = PyObject_CallObject((PyObject *)&matrix_type, argsList);

    Py_DECREF(argsList);

    return obj;
}

PyObject *matrix_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    matrixobject *self;
    self = (matrixobject *)type->tp_alloc(type, 0);

    if (self != NULL)
    {
        for(unsigned int i = 0; i < 16; i++) {
            self->elements[i] = 0;
        }
    }

    return (PyObject *)self;
}

void matrix_dealloc(matrixobject *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

int matrix_init(matrixobject *self, PyObject *args, PyObject *kwds)
{
    PyObject *elementsArray = NULL;

    if (!PyArg_ParseTuple(args, "|O", &elementsArray))
    {
        PyErr_SetString(PyExc_TypeError, "pythree.Matrix(elements: list[float] = None): Expected one optional list of floats.\n"
                                         "pythree.Matrix(elements: list[list[float]] = None): Expected one optional list of floats.");
        return -1;
    }

    if(elementsArray != NULL)
    {
        // Check that elements is "list" or "tuple"
        if(PySequence_Check(elementsArray))
        {
            // *****************************************************************************************
            // * Determine whether "elementsArray" is a list of 16 floats or list of lists of 4 floats *
            // *****************************************************************************************
            const unsigned long long size = PySequence_Fast_GET_SIZE(elementsArray);

            switch(size) {
            case 16:
            {
                // "elementsArray" is a list of 16 floats

                for(unsigned int i = 0; i < 16; i++)
                {
                    PyObject *item = PySequence_Fast_GET_ITEM(elementsArray, i);

                    if (PyLong_Check(item))
                    {
                        self->elements[i] = (float)PyLong_AsDouble(item);
                    }
                    else if (PyFloat_Check(item))
                    {
                        self->elements[i] = (float)PyFloat_AS_DOUBLE(item);
                    }
                    else if (PyNumber_Check(item))
                    {
                        // Item is not an "int" or "float", but supports numeric protocol
                        // This case can be useful for non-standart numeric types, like "numpy.int64", etc.
                        self->elements[i] = (float)PyFloat_AS_DOUBLE(PyNumber_Float(item));
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "pythree.Matrix(elements: list[float] = None): Expected \"float\" or \"int\" in \"elements[%u]\", but got \"%s\".", i, type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return -1;
                    }
                }

                break;
            }

            case 4:
            {
                // "elementsArray" is a list of lists of 4 floats

                for(unsigned int i = 0; i < 4; i++)
                {
                    PyObject *row = PySequence_Fast_GET_ITEM(elementsArray, i);

                    if (PySequence_Check(row))
                    {
                        const unsigned long long rowSize = PySequence_Fast_GET_SIZE(row);

                        if (rowSize == 4)
                        {
                            for(unsigned int j = 0; j < 4; j++)
                            {
                                PyObject *item = PySequence_Fast_GET_ITEM(row, j);

                                if (PyLong_Check(item))
                                {
                                    self->elements[j + i * 4] = (float)PyLong_AsDouble(item);
                                }
                                else if (PyFloat_Check(item))
                                {
                                    self->elements[j + i * 4] = (float)PyFloat_AS_DOUBLE(item);
                                }
                                else if (PyNumber_Check(item))
                                {
                                    // Item is not an "int" or "float", but supports numeric protocol
                                    // This case can be useful for non-standart numeric types, like "numpy.int64", etc.
                                    self->elements[j + i * 4] = (float)PyFloat_AS_DOUBLE(PyNumber_Float(item));
                                }
                                else
                                {
                                    PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                                    char errorMessageBuffer[1024];

                                    sprintf(errorMessageBuffer, "pythree.Matrix(elements: list[float] = None): Expected \"float\" or \"int\" in \"elements[%u][%u]\", but got \"%s\".", i, j, type->tp_name);

                                    PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                                    return -1;
                                }
                            }
                        }
                        else
                        {
                            char errorMessageBuffer[1024];

                            sprintf(errorMessageBuffer, "pythree.Matrix(elements: list[list[float]] = None): \"elements[%u]\" array must have length 4.", i);

                            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                            return -1;
                        }
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject *)PyObject_Type(row);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "pythree.Matrix(elements: list[list[float]] = None): Expected \"list\" or \"tuple\" in \"elements[%u]\", but got \"%s\".", i, type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return -1;
                    }
                }
                break;
            }

            default:
            {
                PyErr_SetString(PyExc_TypeError, "pythree.Matrix(elements: list[float] = None): \"elements\" array must have length 16.\n"
                                                 "pythree.Matrix(elements: list[list[float]] = None): \"elements\" array must have length 4.");
                return -1;
            }
            }
        }
        else
        {
            PyTypeObject *type = (PyTypeObject*)PyObject_Type(elementsArray);
            char errorMessageBuffer[1024];

            sprintf(errorMessageBuffer, "pythree.Matrix(elements: list[float] = None): Expected list, but got \"%s\".\n"
                                        "pythree.Matrix(elements: list[list[float]] = None): Expected list, but got \"%s\".", type->tp_name, type->tp_name);

            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
            return -1;
        }
    }

    return 0;
}

PyObject *matrix_toBytes(matrixobject *self, PyObject *args)
{
    return PyBytes_FromStringAndSize((const char*)self->elements, sizeof(float) * 16);
}

PyObject *matrix_clone(matrixobject *self, PyObject *args)
{
    PyObject *obj = PyMatrix_Create();

    matrixobject *matrix = (matrixobject*)obj;

    for(unsigned int i = 0; i < 16; i++)
    {
        matrix->elements[i] = self->elements[i];
    }

    return obj;
}

// ****************************************
// * Static methods
// ****************************************

PyObject *PyMatrix_fromRotationShiftScale(PyObject *cls, PyObject *args)
{
    PyObject *rotation = NULL;
    PyObject *shift = NULL;
    PyObject *scale = NULL;

    if (!PyArg_ParseTuple(args, "|OOO", &rotation, &shift, &scale))
    {
        PyErr_SetString(PyExc_TypeError, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected three optional lists of floats.\n");
        return NULL;
    }

    PyObject *obj = PyMatrix_Create();
    matrixobject *matrix = (matrixobject*)obj;

    // **********************
    // *    Set rotation    *
    // **********************
    if (rotation != NULL)
    {
        if (PySequence_Check(rotation))
        {
            const unsigned long long size = PySequence_Fast_GET_SIZE(rotation);

            if(size == 3)
            {
                float coords[3];

                for(unsigned int i = 0; i < 3; i++)
                {
                    PyObject *item = PySequence_Fast_GET_ITEM(rotation, i);

                    if (PyLong_Check(item))
                    {
                        coords[i] = (float)PyLong_AsDouble(item);
                    }
                    else if (PyFloat_Check(item))
                    {
                        coords[i] = (float)PyFloat_AS_DOUBLE(item);
                    }
                    else if (PyNumber_Check(item))
                    {
                        // Item is not an "int" or "float", but supports numeric protocol
                        // This case can be useful for non-standart numeric types, like "numpy.int64", etc.
                        coords[i] = (float)PyFloat_AS_DOUBLE(PyNumber_Float(item));
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected \"float\" or \"int\" in \"rotation[%u]\", but got \"%s\".", i, type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return NULL;
                    }
                }

                mat4FromRotation(matrix->elements, coords[0], coords[1], coords[2]);
            }
            else
            {
                PyErr_SetString(PyExc_TypeError, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): \"rotation\" array must have length 3.\n");
                return NULL;
            }
        }
        else
        {
            PyTypeObject *type = (PyTypeObject*)PyObject_Type(rotation);
            char errorMessageBuffer[1024];

            sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected type \"list\" or \"tuple\" in \"rotation\", but got \"%s\".", type->tp_name);

            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
            return NULL;
        }
    }

    // **********************
    // *     Set shift      *
    // **********************
    if (shift != NULL)
    {
        if (PySequence_Check(shift))
        {
            const unsigned long long size = PySequence_Fast_GET_SIZE(shift);

            if(size == 3)
            {
                float coords[3];

                for(unsigned int i = 0; i < 3; i++)
                {
                    PyObject *item = PySequence_Fast_GET_ITEM(shift, i);

                    if (PyLong_Check(item))
                    {
                        coords[i] = (float)PyLong_AsDouble(item);
                    }
                    else if (PyFloat_Check(item))
                    {
                        coords[i] = (float)PyFloat_AS_DOUBLE(item);
                    }
                    else if (PyNumber_Check(item))
                    {
                        // Item is not an "int" or "float", but supports numeric protocol
                        // This case can be useful for non-standart numeric types, like "numpy.int64", etc.
                        coords[i] = (float)PyFloat_AS_DOUBLE(PyNumber_Float(item));
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected \"float\" or \"int\" in \"shift[%u]\", but got \"%s\".", i, type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return NULL;
                    }
                }

                mat4Shift(matrix->elements, coords[0], coords[1], coords[2]);
            }
            else
            {
                PyErr_SetString(PyExc_TypeError, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): \"shift\" array must have length 3.\n");
                return NULL;
            }
        }
        else
        {
            PyTypeObject *type = (PyTypeObject*)PyObject_Type(shift);
            char errorMessageBuffer[1024];

            sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected type \"list\" or \"tuple\" in \"shift\", but got \"%s\".", type->tp_name);

            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
            return NULL;
        }
    }

    // **********************
    // *     Set scale      *
    // **********************
    if (scale != NULL)
    {
        if (PySequence_Check(scale))
        {
            const unsigned long long size = PySequence_Fast_GET_SIZE(scale);

            if(size == 3)
            {
                float coords[3];

                for(unsigned int i = 0; i < 3; i++)
                {
                    PyObject *item = PySequence_Fast_GET_ITEM(scale, i);

                    if (PyLong_Check(item))
                    {
                        coords[i] = (float)PyLong_AsDouble(item);
                    }
                    else if (PyFloat_Check(item))
                    {
                        coords[i] = (float)PyFloat_AS_DOUBLE(item);
                    }
                    else if (PyNumber_Check(item))
                    {
                        // Item is not an "int" or "float", but supports numeric protocol
                        // This case can be useful for non-standart numeric types, like "numpy.int64", etc.
                        coords[i] = (float)PyFloat_AS_DOUBLE(PyNumber_Float(item));
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected \"float\" or \"int\" in \"scale[%u]\", but got \"%s\".", i, type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return NULL;
                    }
                }

                mat4Scale(matrix->elements, coords[0], coords[1], coords[2]);
            }
            else
            {
                PyErr_SetString(PyExc_TypeError, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): \"scale\" array must have length 3.\n");
                return NULL;
            }
        }
        else
        {
            PyTypeObject *type = (PyTypeObject*)PyObject_Type(scale);
            char errorMessageBuffer[1024];

            sprintf(errorMessageBuffer, "pythree.Matrix.from_rotation_shift_scale(rotation: list[float] = None, shift: list[float] = None, scale: list[float] = None): Expected type \"list\" or \"tuple\" in \"scale\", but got \"%s\".", type->tp_name);

            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
            return NULL;
        }
    }

    return obj;
}

PyObject *PyMatrix_perspective(PyObject *cls, PyObject *args)
{
    float fovy = 90.0f;
    float aspect = 1.0f;
    float near = 0.1f;
    float far = 100.0f;

    if (!PyArg_ParseTuple(args, "|ffff", &fovy, &aspect, &near, &far))
    {
        PyErr_SetString(PyExc_TypeError, "pythree.Matrix.perspective(fovy: float = 90.0, aspect: float = 1.0, near: float = 0.1, far: float = 100.0): Expected four optional floats.");
        return NULL;
    }

    PyObject *obj = PyMatrix_Create();
    matrixobject *matrix = (matrixobject*)obj;

    mat4FromPerspective(matrix->elements, fovy, aspect, near, far);

    return obj;
}

PyObject *PyMatrix_identity(PyObject *cls, PyObject *args)
{
    PyObject *obj = PyMatrix_Create();
    matrixobject *matrix = (matrixobject*)obj;

    mat4FromIdentity(matrix->elements);

    return obj;
}

}
