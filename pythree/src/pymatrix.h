#ifndef PYMATRIX_H
#define PYMATRIX_H

#include <Python.h>
#include <structmember.h>
#define PyMatrix_Check(o) PyObject_TypeCheck(o, &matrix_type)

extern "C"
{
    extern PyTypeObject matrix_type;

    typedef struct
    {
        PyObject_HEAD
        float elements[16];
    } matrixobject;

    extern PyObject *matrix_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
    extern void matrix_dealloc(matrixobject *self);
    extern int matrix_init(matrixobject *self, PyObject *args, PyObject *kwds);

    extern PyObject *matrix_toBytes(matrixobject *self, PyObject *args);
    extern PyObject *matrix_clone(matrixobject *self, PyObject *args);
//    extern PyObject *matrix_rotate(matrixobject *self, PyObject *args);
//    extern PyObject *matrix_shift(matrixobject *self, PyObject *args);
//    extern PyObject *matrix_scale(matrixobject *self, PyObject *args);

    extern PyObject *PyMatrix_fromRotationShiftScale(PyObject *cls, PyObject *args);
    extern PyObject *PyMatrix_perspective(PyObject *cls, PyObject *args);
    extern PyObject *PyMatrix_identity(PyObject *cls, PyObject *args);
}

#endif // PYMATRIX_H
