from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as f:
#     desc = f.read()

setup(
    name="pypexel",
    version="0.1.1",
    author="James Richmond",
    author_email="jamcamcode@gmail.com",
    description="A modern, comprehensive Python wrapper for the Pexels API",
    # long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/JRichm/pypexel",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.32.4",
        "python-dotenv>=1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "twine>=3.0",
        ],
    },
    keywords="pexels api photos videos stock images wrapper",
    project_urls={
        "Bug Reports": "https://github.com/JRichm/pypexel/issues",
        "Source": "https://github.com/JRichm/pypexel",
        "Documentation": "https://github.com/JRichm/pypexel#readme",
    },
)