#!/usr/bin/env python

from bob.db.oulunpu import Database

oulunpu_directory = "[OULUNPU_DIRECTORY]"

database = Database(
    original_directory=oulunpu_directory,
)
