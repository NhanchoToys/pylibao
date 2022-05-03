from os import getenv, path
from setuptools import setup, Extension

ext = Extension(
    'pyao._aointernal',
    sources=['pyao/_aointernal.c'],
    libraries=['ao', 'm'],
    library_dirs=[path.join(getenv('PREFIX', '/usr'), 'lib', 'ao')],
    include_dirs=[path.join(getenv('PREFIX', '/usr'), 'include', 'ao')],
)


setup(
    name='pylibao',
    version='0.1.1',
    description='Python library for accessing the Libao API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HivertMoZara',
    author_email='worldmozara@gmail.com',
    url='https://github.com/NCBM/pyao',
    packages=['pyao'],
    ext_modules=[ext],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='audio',
    license='MIT',
)
