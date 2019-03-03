import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name='kairos',
    version='0',
    scripts=['kairos'],
    author="MutatedFlood",
    author_email="b06901038@g.ntu.edu.tw",
    description="A command line weather app.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="weather",
    url="https://github.com/MutatedFlood/KaiRoS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
