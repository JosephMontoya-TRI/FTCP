from setuptools import setup, find_packages
import warnings

DESCRIPTION = "FTCP"

LONG_DESCRIPTION = """
Lorem ipsum
"""

setup(
    name="ftcp",
    version="0.0",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    # install_requires=[
    #     "matminer==0.6.4",
    #     "scikit-learn==0.23.2",
    #     "plotly==4.13.0",
    #     "pymatgen"
    #     ],
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
    ],
    include_package_data=True,
    )
