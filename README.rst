===============
lovd_downloader
===============


.. .. image:: https://img.shields.io/pypi/v/lovd_downloader.svg
..         :target: https://pypi.python.org/pypi/lovd_downloader

.. image:: https://travis-ci.com/kidsneuro-lab/lovd_downloader.svg?token=EpL6q11iM5fdJG4ZMg8X&branch=master
        :target: https://travis-ci.com/h-joshi/lovd_downloader

.. .. image:: https://readthedocs.org/projects/lovd-downloader/badge/?version=latest
..         :target: https://lovd-downloader.readthedocs.io/en/latest/?badge=latest
..         :alt: Documentation Status




Toolset to download variants data from LOVD


* Free software: MIT license
.. * Documentation: https://lovd-downloader.readthedocs.io.

Installation
--------
* Download latest `Release <https://github.com/kidsneuro-lab/lovd_downloader/releases>`_
* Ensure you are installing this in a virtual environment
* Requires Python >= 3.6

Features
--------
* Download unique variants from https://databases.lovd.nl
* **IMPORTANT**: LOVD is a shared resource. The script is not to be used for continuous bulk download of variants. This will put load on LOVD servers and you could get blocked

Typical usage
----------------
Download list of transcripts. Used when downloading variants to check:

* That the gene (or genes) exist on LOVD
* Ignore any genes that don't have annotated variants (to reduce runtime)

``lovd_tx_map -u "https://databases.lovd.nl" -o transcripts.tsv``

Download variants for a given gene

``lovd_variants -u "https://databases.lovd.nl" -o variants.tsv -t transcripts.tsv -g "CAPN3,DYSF"``

Download variants for a all genes

``lovd_variants -u "https://databases.lovd.nl" -o variants.tsv -t transcripts.tsv``

TODO
--------
* Probably more automated tests
* Publish on PyPi
* Add documentation

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
