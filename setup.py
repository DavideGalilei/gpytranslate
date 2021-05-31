import setuptools

with open("README.md", "r", encoding="utf8") as readme, open(
        "requirements.txt", "r", encoding="utf8"
) as requirements:
    long_description = readme.read()
    requires = requirements.read().splitlines(keepends=False)

setuptools.setup(
    name="gpytranslate",
    version="1.2.0",
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
    python_requires=">=3.6",
    install_requires=requires,
)
