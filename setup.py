from setuptools import setup, find_packages

setup(
    name="buoys",
    author="Chris Walsh",
    author_email="chris.is.rad@pm.me",
    classifiers=[],
    description="Queries NOAA's National Buoy Database for datah",
    license="MIT",
    version="0.0.1",
    url="",
    packages=find_packages(),
    install_requires=[
        'tinydb', 'matplotlib', 'numpy'
    ],
    entry_points={
        'console_scripts': [
            'buoys = buoydata.main:boot_up'
        ]
    }
)