from setuptools import setup, find_packages
setup(
    name="Speller",
    version="0.1",
    packages=find_packages(exclude=['test.*']),
    scripts=['say_hello.py'],
    install_requires = [
        'PyQt5',
        'pyphonetics'
    ],
    package_data = {
        # Include database in installation
        'db': ['data.db'],
    },

    # metadata for upload to PyPI
    author="Jake Faulkner",
    author_email="jakefaulkn@gmail.com",
    description="Spell checking software built around individual needs, primarily for dyslexic spellers",
    license="MIT",
    keywords="spelling",
    # could also include long_description, download_url, classifiers, etc.
)
