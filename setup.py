
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(".version", "r") as fh:
    currentVersion = fh.read()

setuptools.setup(
    name="ansiesc_colors",
    version=currentVersion,
    author="Dario Gerosa",
    author_email="dario.gerosa@eis-tech.it",
    description="A small (bean) package about ANSI Escape Codes for colors",
    long_description=f"{long_description}",
    long_description_content_type="text/markdown",
    url="https://github.com/djer0325/ansiesc-colors",
    packages=setuptools.find_packages(exclude=("mylib..old",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',
    include_package_data=True,
    requires=["subprocess", "threading", "shlex", "re"],
    # install_requires=['subprocess', 'threading', 'shlex', 're'],
)
