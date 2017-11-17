# Marvinbot Meme Plugin

Meme Generator

# Requirements

-   A working [Marvinbot](https://github.com/BotDevGroup/marvin) install

-	Pillow [Building](http://pillow.readthedocs.io/en/3.4.x/installation.html#building-from-source) install

# Getting Started

## Install external libraries

The plugin need this library:

- libtiff5
- libjpeg
- zlib1g
- libfreetype6

### Linux (Debian)

	apt-get install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev

### Linux (Arch)

	pacman -S libtiff libjpeg-turbo zlib freetype2

### macOS

	brew install libtiff libjpeg webp little-cms2

### FreeBSD

	pkg install jpeg tiff webp lcms2 freetype2

## Install Plugin

	python setup.py develop