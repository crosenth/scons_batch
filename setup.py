import setuptools

setuptools.setup(author='Chris Rosenthal',
                 author_email='crosenth@gmail.com',
                 classifiers=[
                     'License :: OSI Approved :: '
                     'GNU General Public License v3 (GPLv3)',
                     'Development Status :: 4 - Beta',
                     'Programming Language :: Python :: 3 :: Only'],
                 python_requires='>=3.3',
                 description='SCons Aws Batch plugin',
                 install_requires=['aws_batch>=0.6', 'scons>=3.1.1'],
                 keywords=['aws', 'batch', 's3', 'scons'],
                 license='GPLv3',
                 name='scons_batch',
                 py_modules=['scons_batch'],
                 version=0.2,
                 url='https://github.com/crosenth/scons_batch'
                 )
