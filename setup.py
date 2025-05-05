# setup.py

"""
Setup script for the Memory Optimizer package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="memory-optimizer",
    version="1.0.0",
    author="PavelGuzenfeld",
    author_email="pavel.guzenfeld@example.com",
    description="A CLI tool for optimizing Python code for memory efficiency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PavelGuzenfeld/memory-optimizer",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.1",
    install_requires=[
        "memory-profiler>=0.58.0",
        "numpy>=1.19.5",
        "psutil>=5.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "pytest-mock>=3.6.0",
            "pytest-benchmark>=3.4.0",
            "flake8>=3.8.0",
            "black>=20.8b1",
            "isort>=5.6.0",
            "mypy>=0.800",
            "sphinx>=3.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "types-setuptools>=57.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "memopt=memory_optimizer.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        'memory_optimizer': ['py.typed'],
    },
    project_urls={
        "Bug Reports": "https://github.com/PavelGuzenfeld/memory-optimizer/issues",
        "Documentation": "https://memory-optimizer.readthedocs.io/",
        "Source Code": "https://github.com/PavelGuzenfeld/memory-optimizer",
    },
    keywords="memory optimization python cli development-tools",
)
