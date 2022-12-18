#include <vector>
#include "pygeometry.h"

extern "C" {

PyObject *geometry_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    geometryobject *self;
    self = (geometryobject *)type->tp_alloc(type, 0);

    if (self != NULL)
    {
        self->vertices = std::vector<float> (0);
        self->normals = std::vector<float> (0);
        self->uvs = std::vector<float> (0);
    }

    return (PyObject *)self;
}

void geometry_dealloc(geometryobject *self)
{
    self->vertices.clear();
    self->normals.clear();
    self->uvs.clear();

    Py_TYPE(self)->tp_free((PyObject *)self);
}

int geometry_init(geometryobject *self, PyObject *args, PyObject *kwds)
{
    PyObject *vertices = NULL;
    PyObject *uvs = NULL;
    PyObject *normals = NULL;

    if (!PyArg_ParseTuple(args, "|OOO", &vertices, &uvs, &normals))
    {
        PyErr_SetString(PyExc_TypeError, "Expected three optional arguments.");
        return -1;
    }

    // Get variables by keywords if they weren't provided by args

    if(vertices == NULL && PyMapping_HasKeyString(kwds, "vertices"))
    {
        vertices = PyMapping_GetItemString(kwds, "vertices");
    }

    if(uvs == NULL && PyMapping_HasKeyString(kwds, "uvs"))
    {
        uvs = PyMapping_GetItemString(kwds, "uvs");
    }

    if(normals == NULL && PyMapping_HasKeyString(kwds, "normals"))
    {
        normals = PyMapping_GetItemString(kwds, "normals");
    }

    // Set values from provided arrays
    if(vertices != NULL)
    {
        // Check that provided "vertices" argument has array-like type
        if(PySequence_Check(vertices))
        {
            // "vertices" is array
            Py_ssize_t verticesSize = PySequence_Size(vertices);

            if(verticesSize >= 0)
            {
                self->vertices.resize(verticesSize);

                // Copy values
                for(unsigned int i = 0; i < verticesSize; i++)
                {
                    PyObject *value = PySequence_ITEM(vertices, i);

                    if(PyFloat_Check(value))
                    {
                        self->vertices[i] = PyFloat_AsDouble(value);
                    }
                    else if(PyLong_Check(value))
                    {
                        self->vertices[i] = PyLong_AsDouble(value);
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return -1;
                    }
                }
            }
        }
        else
        {
            // "vertices" is something else
            PyErr_SetString(PyExc_TypeError, "Provided \"vertices\" is not array-like object.");
            return -1;
        }
    }

    if(normals != NULL)
    {
        // Check that provided "normals" argument has array-like type
        if(PySequence_Check(normals))
        {
            // "normals" is array
            Py_ssize_t normalsSize = PySequence_Size(normals);

            if(normalsSize >= 0)
            {
                self->normals.resize(normalsSize);

                // Copy values
                for(unsigned int i = 0; i < normalsSize; i++)
                {
                    PyObject *value = PySequence_ITEM(normals, i);

                    if(PyFloat_Check(value))
                    {
                        self->normals[i] = PyFloat_AsDouble(value);
                    }
                    else if(PyLong_Check(value))
                    {
                        self->normals[i] = PyLong_AsDouble(value);
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return -1;
                    }
                }
            }
        }
        else
        {
            // "normals" is something else
            PyErr_SetString(PyExc_TypeError, "Provided \"normals\" is not array-like object.");
            return -1;
        }
    }

    if(uvs != NULL)
    {
        // Check that provided "uvs" argument has array-like type
        if(PySequence_Check(uvs))
        {
            // "uvs" is array
            Py_ssize_t uvsSize = PySequence_Size(uvs);

            if(uvsSize >= 0)
            {
                self->uvs.resize(uvsSize);

                // Copy values
                for(unsigned int i = 0; i < uvsSize; i++)
                {
                    PyObject *value = PySequence_ITEM(uvs, i);

                    if(PyFloat_Check(value))
                    {
                        self->uvs[i] = PyFloat_AsDouble(value);
                    }
                    else if(PyLong_Check(value))
                    {
                        self->uvs[i] = PyLong_AsDouble(value);
                    }
                    else
                    {
                        PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                        char errorMessageBuffer[1024];

                        sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                        PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                        return -1;
                    }
                }
            }
        }
        else
        {
            // "uvs" is something else
            PyErr_SetString(PyExc_TypeError, "Provided \"uvs\" is not array-like object.");
            return -1;
        }
    }

    return 0;
}

/*
**************************************************
** Setters
**************************************************
*/

PyObject *geometry_setVertices(geometryobject *self, PyObject *args)
{
    PyObject *vertices;

    if (!PyArg_ParseTuple(args, "O", &vertices))
    {
        PyErr_SetString(PyExc_TypeError, "pythree.Geometry.set_vertices(vertices: list[float]): Expected one or two arguments.");
        return NULL;
    }

    // Check that provided "vertices" argument has array-like type
    if(PySequence_Check(vertices))
    {
        // "vertices" is array
        Py_ssize_t verticesSize = PySequence_Size(vertices);

        if(verticesSize >= 0)
        {
            self->vertices.resize(verticesSize);

            // Copy values
            for(unsigned int i = 0; i < verticesSize; i++)
            {
                PyObject *value = PySequence_ITEM(vertices, i);

                if(PyFloat_Check(value))
                {
                    self->vertices[i] = PyFloat_AsDouble(value);
                }
                else if(PyLong_Check(value))
                {
                    self->vertices[i] = PyLong_AsDouble(value);
                }
                else
                {
                    PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                    char errorMessageBuffer[1024];

                    sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                    PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                    return NULL;
                }
            }
        }
    }
    else
    {
        // "vertices" is something else
        PyErr_SetString(PyExc_TypeError, "Provided value is not array-like object.");
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *geometry_setNormals(geometryobject *self, PyObject *args)
{
    PyObject *normals;

    if (!PyArg_ParseTuple(args, "O", &normals))
    {
        PyErr_SetString(PyExc_TypeError, "Expected one argument.");
        return NULL;
    }

    // Check that provided "normals" argument has array-like type
    if(PySequence_Check(normals))
    {
        // "normals" is array
        Py_ssize_t normalsSize = PySequence_Size(normals);

        if(normalsSize >= 0)
        {
            self->normals.resize(normalsSize);

            // Copy values
            for(unsigned int i = 0; i < normalsSize; i++)
            {
                PyObject *value = PySequence_ITEM(normals, i);

                if(PyFloat_Check(value))
                {
                    self->normals[i] = PyFloat_AsDouble(value);
                }
                else if(PyLong_Check(value))
                {
                    self->normals[i] = PyLong_AsDouble(value);
                }
                else
                {
                    PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                    char errorMessageBuffer[1024];

                    sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                    PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                    return NULL;
                }
            }
        }
    }
    else
    {
        // "normals" is something else
        PyErr_SetString(PyExc_TypeError, "Provided value is not array-like object.");
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *geometry_setUvs(geometryobject *self, PyObject *args)
{
    PyObject *uvs;

    if (!PyArg_ParseTuple(args, "O", &uvs))
    {
        PyErr_SetString(PyExc_TypeError, "Expected one argument.");
        return NULL;
    }

    // Check that provided "uvs" argument has array-like type
    if(PySequence_Check(uvs))
    {
        // "uvs" is array
        Py_ssize_t uvsSize = PySequence_Size(uvs);

        if(uvsSize >= 0)
        {
            self->uvs.resize(uvsSize);

            // Copy values
            for(unsigned int i = 0; i < uvsSize; i++)
            {
                PyObject *value = PySequence_ITEM(uvs, i);

                if(PyFloat_Check(value))
                {
                    self->uvs[i] = PyFloat_AsDouble(value);
                }
                else if(PyLong_Check(value))
                {
                    self->uvs[i] = PyLong_AsDouble(value);
                }
                else
                {
                    PyTypeObject *type = (PyTypeObject*)PyObject_Type(value);
                    char errorMessageBuffer[1024];

                    sprintf(errorMessageBuffer, "Expected \"float\" or \"int\", but got \"%s\".", type->tp_name);

                    PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                    return NULL;
                }
            }
        }
    }
    else
    {
        // "uvs" is something else
        PyErr_SetString(PyExc_TypeError, "Provided value is not array-like object.");
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}


/*
**************************************************
** Getters
**************************************************
*/

PyObject *geometry_getVertices(geometryobject *self, PyObject *args)
{
    PyObject *tuple = PyTuple_New(self->vertices.size());

    for(unsigned int i = 0; i < self->vertices.size(); i++)
    {
        PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(self->vertices[i]));
    }

    return tuple;
}

PyObject *geometry_getNormals(geometryobject *self, PyObject *args)
{
    PyObject *tuple = PyTuple_New(self->normals.size());

    for(unsigned int i = 0; i < self->normals.size(); i++)
    {
        PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(self->normals[i]));
    }

    return tuple;
}

PyObject *geometry_getUvs(geometryobject *self, PyObject *args)
{
    PyObject *tuple = PyTuple_New(self->uvs.size());

    for(unsigned int i = 0; i < self->uvs.size(); i++)
    {
        PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(self->uvs[i]));
    }

    return tuple;
}


/*
**************************************************
** Bytes getters
**************************************************
*/

PyObject *geometry_getVerticesAsBytes(geometryobject *self, PyObject *args)
{
    return PyBytes_FromStringAndSize((char*)self->vertices.data(), self->vertices.size() * sizeof(float));
}

PyObject *geometry_getNormalsAsBytes(geometryobject *self, PyObject *args)
{
    return PyBytes_FromStringAndSize((char*)self->normals.data(), self->normals.size() * sizeof(float));
}

PyObject *geometry_getUvsAsBytes(geometryobject *self, PyObject *args)
{
    return PyBytes_FromStringAndSize((char*)self->uvs.data(), self->uvs.size() * sizeof(float));
}

}
