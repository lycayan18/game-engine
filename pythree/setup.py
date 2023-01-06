from distutils.core import setup, Extension


def main():
    setup(name="pythree",
          version="0.0.0",
          description="Python 3d lib",
          author="DungyBug",
          author_email="",
          ext_modules=[Extension("pythree", sources=["src/matrix.cpp", "src/pymatrix.cpp", "src/pygeometry.cpp", "src/main.cpp"], extra_compile_args=["/std:c++20"])])


if __name__ == "__main__":
    main()
