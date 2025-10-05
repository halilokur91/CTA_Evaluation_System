"""
CTA Evaluation System Installation Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cta-evaluation-system",
    version="1.0.0",
    author="Halil Ibrahim Okur",
    author_email="hibrahim.okur@iste.edu.tr",
    description="Common Turkic Alphabet (CTA) Academic Research Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/halilokur91/cta-evaluation-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cta-eval=main:main",
        ],
    },
    keywords="turkic languages, transliteration, phonetics, linguistics, alphabet, research",
    project_urls={
        "Bug Reports": "https://github.com/halilokur91/cta-evaluation-system/issues",
        "Source": "https://github.com/halilokur91/cta-evaluation-system",
        "Documentation": "https://github.com/halilokur91/cta-evaluation-system/wiki",
    },
)
