#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Test Units
"""
from bob.db.oulunpu import Database


def assert_nfiles(files, total, nbonafide, nattack):
    len_files = len(files)
    assert len_files == total, len_files
    len_bonafide = len([f for f in files if f.attack_type is None])
    len_attack = len_files - len_bonafide
    assert len_bonafide == nbonafide, len_bonafide
    assert len_attack == nattack, len_attack


def test_database():
    db = Database(protocol='Protocol_1')
    assert len(db.all_files())
    assert_nfiles(db.objects(), 1200 + 900 + 600,
                  240 + 180 + 120 + 480, 960 + 720)
    assert_nfiles(db.objects(groups='world'), 1200, 240, 960)
    assert_nfiles(db.objects(groups='dev'), 900, 180, 720)
    assert_nfiles(db.objects(groups='eval'), 600, 120 + 480, 0)

    db = Database(protocol='Protocol_2')
    assert_nfiles(db.objects(), 1080 * 2 + 810,
                  360 + 270 + 360 + 720, 720 + 540)
    assert_nfiles(db.objects(groups='world'), 1080, 360, 720)
    assert_nfiles(db.objects(groups='dev'), 810, 270, 540)
    assert_nfiles(db.objects(groups='eval'), 1080, 360 + 720, 0)

    for i in range(1, 7):
        db = Database(protocol='Protocol_3_{}'.format(i))
        assert_nfiles(db.objects(), 1500 + 1125 + 300,
                      300 + 225 + 60 + 240, 1200 + 900)
        assert_nfiles(db.objects(groups='world'), 1500, 300, 1200)
        assert_nfiles(db.objects(groups='dev'), 1125, 225, 900)
        assert_nfiles(db.objects(groups='eval'), 300, 60 + 240, 0)

        db = Database(protocol='Protocol_4_{}'.format(i))
        assert_nfiles(db.objects(), 600 + 450 + 60,
                      200 + 150 + 20 + 40, 400 + 300)
        assert_nfiles(db.objects(groups='world'), 600, 200, 400)
        assert_nfiles(db.objects(groups='dev'), 450, 150, 300)
        assert_nfiles(db.objects(groups='eval'), 60, 20 + 40, 0)
