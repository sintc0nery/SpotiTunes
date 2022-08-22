from importlib.metadata import entry_points
from setuptools import setup,find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spotitunes',
    version='0.1.0',
    author='SCervino',
    author_email='scervinosanchez@gmail.com',
    description='Compares desired playlists of iTunes versus Spotify.',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'SpotiTunes=spotitunes.menu:main'
        ],
    },
    install_requires=[
        "spotipy>=2.20.0",
        "unidecode",
        "pyfiglet",
        "prettytable",
        "argparse",
        "deemix",
        "six>=1.15.0",
        "libpytunes @ git+https://github.com/sintc0nery/libpytunes.git",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)