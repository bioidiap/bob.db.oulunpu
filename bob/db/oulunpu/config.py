#!/usr/bin/env python

from bob.db.oulunpu import Database
from bob.pad.base.pipelines.vanilla_pad.legacy import DatabaseConnector
database = DatabaseConnector(Database(protocol='Protocol_1'))
