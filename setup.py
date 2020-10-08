from setuptools import setup, find_namespace_packages

setup(
    name="ts-devtools",
    packages=find_namespace_packages(include=["tetrascience.*"]),
    install_requires=["typing_extensions", "jsonschema"],
)
