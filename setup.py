"""
Elementwise provides convenient proxy objects which build operation chains 
generatively. create chain on an iterable which transforms
operator behavior, function and methods into vectorized versions which operate
on all members of the iterable.
"""

from distutils.core import setup

setup(
    name="constraints",
    packages=["constraints"],
    author="Nathan Rice",
    author_email="nathan.alexander.rice@gmail.com",
    version="0.120126",
    license="BSD 2 clause",
    include_package_data=True,
    zip_safe=False,
    install_requires=["decorator"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
