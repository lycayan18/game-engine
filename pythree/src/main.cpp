#define PY_SSIZE_T_CLEAN
#define PY_NO_LINK_LIB
#include "pythree.h"

extern "C"
{
    static struct PyModuleDef pythreemodule = {
        .m_base = PyModuleDef_HEAD_INIT,
        .m_name = "pythree",
        .m_doc = "Library for working with 3d",
        .m_size = -1
    };

    /*
    ***************************************************
    **  Geometry class
    ***************************************************
    */

    static PyMethodDef geometry_methods[] = {
        {"set_normals",             (PyCFunction)geometry_setNormals,           METH_VARARGS,   PyDoc_STR("Set normals array")},
        {"set_vertices",            (PyCFunction)geometry_setVertices,          METH_VARARGS,   PyDoc_STR("Set vertices array")},
        {"set_uvs",                 (PyCFunction)geometry_setUvs,               METH_VARARGS,   PyDoc_STR("Set uvs array")},
        {"get_normals",             (PyCFunction)geometry_getNormals,           METH_NOARGS,    PyDoc_STR("Get normals array")},
        {"get_vertices",            (PyCFunction)geometry_getVertices,          METH_NOARGS,    PyDoc_STR("Get vertices array")},
        {"get_uvs",                 (PyCFunction)geometry_getUvs,               METH_NOARGS,    PyDoc_STR("Get uvs array")},
        {"get_normals_as_bytes",    (PyCFunction)geometry_getNormalsAsBytes,    METH_NOARGS,    PyDoc_STR("Get normals array as bytes")},
        {"get_vertices_as_bytes",   (PyCFunction)geometry_getVerticesAsBytes,   METH_NOARGS,    PyDoc_STR("Get vertices array as bytes")},
        {"get_uvs_as_bytes",        (PyCFunction)geometry_getUvsAsBytes,        METH_NOARGS,    PyDoc_STR("Get uvs array as bytes")},
        {NULL, NULL, 0, NULL}
    };

    static struct PyMemberDef geometry_members[] = {
        {NULL}
    };

    extern PyTypeObject geometry_type = {
        .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "pythree.Geometry",
        .tp_basicsize = sizeof(geometryobject),
        .tp_itemsize = 0,
        .tp_dealloc = (destructor)geometry_dealloc,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        .tp_methods = geometry_methods,
        .tp_members = geometry_members,
        .tp_init = (initproc)geometry_init,
        .tp_new = geometry_new,
    };

    PyMODINIT_FUNC
    PyInit_pythree(void)
    {
        PyObject *m;

        if (PyType_Ready(&geometry_type) < 0)
            return NULL;

        m = PyModule_Create(&pythreemodule);

        if (m == NULL)
            return NULL;

        Py_INCREF(&geometry_type);

        if (PyModule_AddObject(m, "Geometry", (PyObject *)&geometry_type) < 0)
        {
            Py_DECREF(&geometry_type);
            Py_DECREF(m);

            return NULL;
        }

        return m;
    }
};
