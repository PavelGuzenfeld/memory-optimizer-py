"""
Setup script for the Memory Optimizer package.
"""

from setuptools import setup, find_packages

setup(
    name="memory-optimizer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for optimizing Python code for memory efficiency",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/memory-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8.1",
    install_requires=[
        "memory-profiler>=0.58.0",
        "numpy>=1.19.5",
        "psutil>=5.8.0",
    ],
    entry_points={
        "console_scripts": [
            "memopt=memory_optimizer.cli:main",
        ],
    },
    include_package_data=True,
)