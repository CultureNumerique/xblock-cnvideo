import os
from setuptools import setup

def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`.""" 
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))
  
    return {pkg: data}

setup(
    name='xblock-cnvideo',
    version='0.1.4',
    description='plugin pour importer des videos dans un cours',
    #py_modules=['cnvideo'],
    packages=['cnvideo'],
    install_requires=['XBlock'],
    entry_points={
        'xblock.v1':['cnvideo = cnvideo:CNVideoBlock',]
    },
    package_data=package_data("cnvideo", "static")
)

