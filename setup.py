from setuptools import setup, find_packages

# metadata...
name = "agntsmth-core"
description = (
    "A simple agentic workflow builder framework, ontop of LangChain and LangGraph."
)
author = "Simon Stipcich"
author_email = "stipcich.simon@gmail.com"
url = "https://github.com/stiproot/agntsmth-core"
license = "MIT"
keywords = ["python", "package", "langchain", "langgraph", "agentic", "beta"]
version = "0.1.4"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# dependencies...
install_requires = [
    "environs",
    "langchain",
    "langchain-chroma",
    "langchain-openai",
    "langchain-community",
    "bs4",
    "chromadb",
    "langgraph",
    "IPython",
    "pydantic",
    "rich",
]

# setup...
setup(
    name=name,
    version=version,
    packages=find_packages(where="src"),
    package_dir={"agntsmth_core": "src/agntsmth_core"},
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    keywords=keywords,
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)
