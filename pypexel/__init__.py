"""
PyPexel - A modern Python wrapper for the Pexels API

A comprehensive, easy-to-use library for accessing Pexels' vast collection
of royalty-free photos and videos through their API.
"""

from .pypexel import Pexels, PexelsAPIError


__version__ = "0.1.0"
__author__ = "James Richmond"
__email__ = "jamcamcode@gmail.com"
__license__ = "MIT"

# Make main classes available at package level
__all__ = ["Pexels", "PexelsAPIError"]

# Package metadata
__title__ = "pypexel"
__description__ = "A modern, comprehensive Python wrapper for the Pexels API"
__url__ = "https://github.com/JRichm/pypexel"