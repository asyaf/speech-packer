import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speech-packer-asyaf",
    version="1.0.0",
    author="asyaf",
    description="A tool for creating a packing list using speech recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asyaf/speech",
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.6',
)