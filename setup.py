from setuptools import setup

setup(
    name="updatr",
    packages=[
        "updatr",
    ],
    install_requires=[
        "wheel",
        "osxphotos",
        "flickrapi",
        "pyyaml>=5.3",
    ],
    python_requires=">=3.9.0",
    include_package_data=False,
    exclude_package_data={
        "": ["updatr.egg-info", "__pycache__", ".DS_Store", "docs"]
    },
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "updatr = updatr.updatr:main",
        ]
    },
    version='0.0.1',
    description="""Flickr Updater for photo compilations""",
    author="Dirk Roorda",
    author_email="dirk.roorda@icloud..com",
    url="https://github.com/dirkroorda/historisch-eefde",
    keywords=[
        "photos",
        "metadata",
        "flickr",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    long_description="""\
Manage a photo collection in macos Photos and then sync it to Dropbox and Flickr,
including metadata and album organization.
""",
)
