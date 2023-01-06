#ifndef PYGEOMETRY_H
#define PYGEOMETRY_H

#include <vector>

#include <Python.h>
#include <structmember.h>
#define PyGeometry_Check(o) PyObject_TypeCheck(o, &geometry_type)

extern "C"
{
    extern PyTypeObject geometry_type;

    typedef struct
    {
        PyObject_HEAD
        std::vector<float> vertices;
        std::vector<float> normals;
        std::vector<float> uvs;
    } geometryobject;

    extern PyObject *geometry_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
    extern void geometry_dealloc(geometryobject *self);
    extern int geometry_init(geometryobject *self, PyObject *args, PyObject *kwds);

    extern PyObject *geometry_setVertices(geometryobject *self, PyObject *args);
    extern PyObject *geometry_setNormals(geometryobject *self, PyObject *args);
    extern PyObject *geometry_setUvs(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getVertices(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getNormals(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getUvs(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getVerticesAsBytes(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getNormalsAsBytes(geometryobject *self, PyObject *args);
    extern PyObject *geometry_getUvsAsBytes(geometryobject *self, PyObject *args);
}

#endif // PYGEOMETRY_H
