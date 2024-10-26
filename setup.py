from setuptools import setup, find_packages

# metadata...
name = "agnt_smth"
description = (
    "A simple agentic workflow builder framework, ontop of LangChain and LangGraph."
)
author = "Simon Stipcich"
author_email = "stipcich.simon@gmail.com"
url = "https://github.com/stiproot/agnt-smth"
license = "MIT"
keywords = ["python", "package", "lang-chain", "lang-graph" "beta"]
version = "0.1.2"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# dependencies...
install_requires = [
    "langchain",
    "langchain-community",
    "langchainhub",
    "langchain-chroma",
    "langchain-openai",
    "langchain-huggingface",
    "bs4",
    "chromadb",
    "sentence-transformers",
    "langgraph",
    "langsmith",
    "IPython",
    "pydantic",
    "rich",
]

# setup...
setup(
    name=name,
    version=version,
    packages=find_packages(where="src"),
    package_dir={"agnt_smth": "src/agnt_smth"},
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
        "Programming Language :: Python :: 3.11",
    ],
)
