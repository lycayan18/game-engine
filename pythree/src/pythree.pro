TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
        main.cpp \
        matrix.cpp \
        pygeometry.cpp \
        pymatrix.cpp

INCLUDEPATH += C:/Python310/include/

HEADERS += \
    C:/Python310/include/Python.h \
    matrix.h \
    pygeometry.h \
    pymatrix.h \
    pythree.h
