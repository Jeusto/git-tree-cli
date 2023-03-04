import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gittree",
    version="0.0.1",
    author="Jeusto",
    author_email="contact@jeusto.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jeusto/gittree",
    project_urls={
        "Homepage": "http://gittree.jeusto.com",
        "Bug Tracker": "https://github.com/jeusto/gittree/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
