from setuptools import find_packages, setup

setup(
    name="TimeTableLib",
    packages=find_packages(include=["managers", "managers.common"]),
    version="v0.1.0",
    description="This Library generates timetable and is a plug and play solution for any python based backend service.",
    long_description=open("README.md").read(),
    authors=["GEHU, Bhimtal"],
    license="MIT",
    install_requires=[
        "psycopg2-binary==2.9.9",
        "pytest==7.4.2",
    ],  # noqa: E501
    setup_requires=["pytest-runner"],
    tests_require=["pytest==7.4.2"],
    test_suite="tests",
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://github.com/TImeTable-GEHU/Time-Table/blob/main/README.md",
        "Source": "https://github.com/TImeTable-GEHU/Time-Table",
    },
)