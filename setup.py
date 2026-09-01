"""Setup script for uigen C extension."""

from setuptools import Extension, setup

cext = Extension(
    "uigen._cext",
    sources=["src/uigen/_cext.c"],
    extra_compile_args=["-O3", "-march=native"],
)

setup(
    ext_modules=[cext],
)
