import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpytranslate",
    version="0.1.2",
    author="Davide Galilei",
    author_email="davidegalilei2018@gmail.com",
    description="A Python3 library for translating text using Google Translate API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DavideGalilei/gpytranslate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
   'httpx',
    ]
)
