import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heyexReader",
    version="0.0.1",
    author="Aaron Lee",
    author_email="leeay@uw.edu",
    description="Python package for reading and parsing Heyex Heidelberg Spectralis OCT files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayl/heyexReader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	"Intended Audience :: Healthcare Industry",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
	"Development Status :: 3 - Alpha"
    ],
)
