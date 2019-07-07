# mkefiboot

This is a "friendly fork" standalone copy of `mkefiboot` that is normally part of [Lorax](https://weldr.io/lorax/).

This project was made for the express purpose of supporting producing EFI boot capable media on Linux distributions
where the full Lorax software package (which requires [Anaconda, the Red Hat/Fedora installer](https://anaconda-installer.readthedocs.io/en/latest/)) would not be available.

`mkefiboot` has the following requirements:

* Python 3
* [`shim`](https://github.com/rhboot/shim) signed by [the Shim Review folks](https://github.com/rhboot/shim-review)
* Distribution signed GRUB 2 EFI binaries
* GNU Parted
* `device-mapper`
* `dosfstools`
* `hfsplus-tools`

## Installing

`mkefiboot` can be installed easily using the included `setup.py`:

```bash

$ python3 setup.py build
$ python3 setup.py install

```
