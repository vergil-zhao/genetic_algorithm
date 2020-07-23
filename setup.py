from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='genetic',
    version='1.0.0',
    author='Vergil Choi',
    author_email='vergil.choi.zyc@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vergilchoi/genetic_algorithm',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['matplotlib', 'click', 'pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Scientific/Engineering',
    ],
    entry_points={
        'console_scripts': [
            'genetic = cli:main'
        ]
    })
