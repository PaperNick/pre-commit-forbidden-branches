import setuptools


setuptools.setup(
    name="pre-commit-forbidden-branches",
    version="0.2.0",
    description="Forbid commits",
    long_description="Pre-commit hook which forbids commiting in a certain set of branches",
    long_description_content_type="text/plain",
    url="https://github.com/PaperNick/pre-commit-forbidden-branches",
    packages=setuptools.find_packages(".", exclude=("tests*", "testing*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    entry_points={
        "console_scripts": ["forbid-commits-hook = pre_commit_hook.forbid_commits:main"]
    },
)
