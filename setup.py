from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="moodgit",
    version="1.0.0",
    author="Sakshi Kale",
    author_email="sakshiskale.2405@gmail.com",
    description="Emotional timeline of your git commits — powered by Claude AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Techie-Sakshi24/moodgit",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.25.0",
        "gitpython>=3.1.0",
        "rich>=13.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "moodgit=moodgit.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="git commits emotions developer-tools ai claude anthropic",
)
