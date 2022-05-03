from distutils.core import setup, Extension
from os import path, getenv

ext = Extension(
    'pyao._aointernal',
    sources=['pyao/_aointernal.c'],
    include_dirs=[
        path.join(getenv('PREFIX', '/usr'), 'include', 'ao'),
    ],
    libraries=['ao', 'm'],
    library_dirs=[path.join(getenv('PREFIX', '/usr'), 'lib', 'ao')],
)

setup(
    name='pylibao',
    version='0.1.0',
    description='Python libao interface',
    author='HivertMoZara',
    author_email='worldmozara@gmail.com',
    url='https://github.com/NCBM/pyao',
    packages=['pyao'],
    ext_modules=[ext],
)
