"""
Setup script for RT-cNEO package.

Install with: pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_file = Path(__file__).parent / "README_NEW.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="rtcneo",
    version="1.0.0",
    author="Federico Zahariev",
    author_email="",
    description="Real-Time constrained Nuclear-Electronic Orbital (RT-cNEO) dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/RT_cNEO",  # Update with actual URL
    packages=find_packages(exclude=["tests", "examples", "archive", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        # PySCF-NEO installed separately (see README)
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
    },
    entry_points={
        "console_scripts": [
            "rtcneo-compare=examples.03_comparison:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rtcneo": ["py.typed"],
    },
    zip_safe=False,
)
