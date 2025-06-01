from setuptools import setup, find_packages

setup(
    name="guardrails-sdk",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python SDK for interacting with the Guardrails API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/guardrails-sdk",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
        "pydantic",
        "torch",
        "transformers",
        "presidio-analyzer",
        "presidio-anonymizer",
        "llm-guard"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)