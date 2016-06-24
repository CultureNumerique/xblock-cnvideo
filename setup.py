from setuptools import setup

setup(
    name='xblock-cnvideo',
    version='0.1',
    description='plugin pour importer des videos dans un cours',
    py_modules=['cnvideo'],
    install_requires=['XBlock'],
    entry_points={
        'xblock.v1':['cnvideo = cnvideo:CNVideoBlock',]
    }
)

