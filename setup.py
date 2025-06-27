from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='subham ulal',
    author_email='subhamulal58@gmail.com',
    install_requires=["openai","langchain","langchain-community","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)