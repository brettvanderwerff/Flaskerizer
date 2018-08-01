import setuptools

with open("README.md", "r") as read_obj:
    long_description = read_obj.read()

setuptools.setup(
    name="flaskerizer",
    version= "0.0.1",
    author="Brett Vanderwerff",
    author_email="brett.vanderwerff@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brettvanderwerff/Flaskerizer",
    packages=setuptools.find_packages(),
    install_requires=[
              'flask',
          ],
    entry_points={
              'console_scripts': [
                  'flaskerizer = flaskerizer.__main__:main'
              ]
          },
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Framework :: Flask",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
        ))
