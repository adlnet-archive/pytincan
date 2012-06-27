from setuptools import find_packages, setup

setup(name="pytincan", 
      version="0.0.1", 
      author="Steve Trevorrow", 
      author_email="streverrow@problemsolutions.net", 
      packages=find_packages(),
      long_description="Python package to interact with the TinCanAPI",
      install_requires=["requests>=0.13.1"])
