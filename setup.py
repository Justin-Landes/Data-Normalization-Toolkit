from setuptools import setup, find_packages

setup(
    name="bmi_analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add dependencies here, like "pandas", "numpy"
    ],
    author="Justin Landes",
    author_email="landesemail@gmail.com",
    description="Smart BMI Analyzer - AI/ML Project Template",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Justin-Landes/bmi-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
