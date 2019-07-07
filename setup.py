#!/usr/bin/python3

from distutils.core import setup

setup(name="mkefiboot",
      version="31.8.0.1", # derived from lorax-31.8
      description="mkefiboot",
      long_description="Tool for producing the efiboot image, forked from Lorax",
      author="Martin Gracik <mgracik@redhat.com>, Will Woods <wwoods@redhat.com>, Brian C. Lane <bcl@redhat.com>",
      author_email="wwoods@redhat.com",
      maintainer="Neal Gompa",
      maintainer_email="ngompa@fedoraproject.org",
      url="https://pagure.io/mkefiboot",
      download_url="https://releases.pagure.org/mkefiboot",
      license="GPLv2+",
      packages=["pymkefiboot"],
      scripts=["bin/mkefiboot"],
      )
