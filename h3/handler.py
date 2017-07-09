import os
from ..hek.handler import HaloHandler
from os.path import abspath, basename, exists, isfile, normpath, splitext

class Halo3Handler(HaloHandler):
    default_defs_path = "reclaimer.h3.defs"
