"""Generic setup.py for Cython code."""
import os
import sys
from distutils.core import setup
from distutils.extension import Extension

USE_CYTHON = '--with-cython' in sys.argv or not os.path.exists(
		'src/roaringbitmap.c')
if USE_CYTHON:
	if '--with-cython' in sys.argv:
		sys.argv.remove('--with-cython')
	try:
		from Cython.Build import cythonize
		from Cython.Distutils import build_ext
	except ImportError:
		raise RuntimeError('could not import Cython.')
	cmdclass = dict(build_ext=build_ext)
else:
	cmdclass = dict()

DEBUG = '--debug' in sys.argv
if DEBUG:
	sys.argv.remove('--debug')

with open('README.rst') as inp:
	README = inp.read()

METADATA = dict(name='roaringbitmap',
		version='0.4pre',
		description='Roaring Bitmap',
		long_description=README,
		author='Andreas van Cranenburgh',
		author_email='A.W.vanCranenburgh@uva.nl',
		url='https://github.com/andreasvc/roaringbitmap/',
		classifiers=[
				'Development Status :: 4 - Beta',
				'Intended Audience :: Science/Research',
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Operating System :: POSIX',
				'Programming Language :: Python :: 2.7',
				'Programming Language :: Python :: 3.3',
				'Programming Language :: Cython',
		],
)

# some of these directives increase performance,
# but at the cost of failing in mysterious ways.
directives = {
		'profile': False,
		'cdivision': True,
		'fast_fail': True,
		'nonecheck': False,
		'wraparound': False,
		'boundscheck': False,
		'embedsignature': True,
		'warn.unused': True,
		'warn.unreachable': True,
		'warn.maybe_uninitialized': True,
		'warn.undeclared': False,
		'warn.unused_arg': False,
		'warn.unused_result': False,
		}

if __name__ == '__main__':
	if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 3):
		raise RuntimeError('Python version 2.7 or >= 3.3 required.')
	os.environ['GCC_COLORS'] = 'auto'
	extra_compile_args = ['-O3', '-march=native', '-DNDEBUG',
			'-Wno-strict-prototypes']
	extra_link_args = ['-DNDEBUG']
	if USE_CYTHON:
		if DEBUG:
			directives.update(wraparound=True, boundscheck=True)
			extra_compile_args = ['-g', '-O0',
					'-Wno-strict-prototypes', '-Wno-unused-function']
			extra_link_args = ['-g']
		ext_modules = cythonize(
				[Extension(
					'*',
					sources=['src/*.pyx'],
					extra_compile_args=extra_compile_args,
					extra_link_args=extra_link_args,
					)],
				annotate=True,
				compiler_directives=directives,
				language_level=3,
		)
	else:
		ext_modules = [Extension(
				'roaringbitmap',
				sources=['src/roaringbitmap.c'],
				extra_compile_args=extra_compile_args,
				extra_link_args=extra_link_args,
				)]
	setup(
			cmdclass=cmdclass,
			ext_modules=ext_modules,
			**METADATA)
