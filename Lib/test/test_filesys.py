"""
Test all filesystem-related modules by using different path types:
- string
- bytes
- non-ascii unicode string
"""

import os
import unittest
from test import support


SPATH = support.TESTFN
BPATH = bytes(SPATH, 'ascii')
UPATH = support.TESTFN_UNICODE
ALL_PATHS = (SPATH, BPATH, UPATH)


# =====================================================================
# utils
# =====================================================================


def safe_rmpath(path):
    try:
        support.unlink(path)
    except IsADirectoryError:
        support.rmtree(path)


def touch(fname):
    with open(fname, "w"):
        pass


class _SinglePathTest(unittest.TestCase):

    def setUp(self):
        for path in ALL_PATHS:
            safe_rmpath(path)

    tearDown = setUp

    def check_file(self, fun, path, **kwargs):
        ret = fun(path, **kwargs)
        if os.path.exists(path):
            assert os.path.isfile(path)
        safe_rmpath(path)
        self.assertRaises(FileNotFoundError, fun, path, **kwargs)
        return ret

    def check_dir(self, fun, path, **kwargs):
        ret = fun(path, **kwargs)
        if os.path.exists(path):
            assert os.path.isdir(path)
        safe_rmpath(path)
        self.assertRaises(FileNotFoundError, fun, path, **kwargs)
        return ret


# =====================================================================
# os.* functions
# =====================================================================


class TestOsSinglePath(_SinglePathTest):
    """Test for all os.* functions accepting a single path.
    https://docs.python.org/3/library/os.html#files-and-directories
    """

    def test_access(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                assert not os.access(path, os.R_OK)
                touch(path)
                assert os.access(path, os.R_OK)
                os.remove(path)

    def test_chdir(self):
        here = os.getcwd()
        try:
            for path in ALL_PATHS:
                with self.subTest(path=path):
                    os.mkdir(path)
                    self.check_dir(os.chdir, path)
        finally:
            os.chdir(here)

    def test_listdir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                self.check_dir(os.listdir, path)

    def test_scandir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                self.check_dir(lambda p: list(os.scandir(p)), path)

    def test_chmod(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                self.check_dir(os.chmod, path, mode=0o777)
                touch(path)
                self.check_file(os.chmod, path, mode=0o777)

    @unittest.skipIf(not hasattr(os, "chflags"), "not supported")
    def test_chflags(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                self.check_dir(os.chflags, path, mode=0o777)
                touch(path)
                self.check_file(os.chflags, path, mode=0o777)

    @unittest.skipIf(not hasattr(os, "chroot"), "not supported")
    @unittest.skipIf(hasattr(os, "getuid") and os.getuid() == 0,
                     "need unprivileged user")
    def test_chroot(self):
        # XXX: perhaps test it in a subprocess?
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_rmpath(path)
                os.mkdir(path)
                try:
                    self.check_dir(os.chroot, path)
                except PermissionError:
                    pass

    def test_remove(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.remove, path)

    def test_rmdir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                self.check_dir(os.rmdir, path)

    def test_removedirs(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                os.mkdir(path)
                os.removedirs(path)

    def test_stat(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.stat, path)
                os.mkdir(path)
                self.check_dir(os.stat, path)

    @unittest.skipIf(not hasattr(os, "statvs"), "not supported")
    def test_statvs(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.statvfs, path)
                os.mkdir(path)
                self.check_dir(os.statvfs, path)

    def test_utime(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.utime, path)
                os.mkdir(path)
                self.check_dir(os.utime, path)

    def test_listxattr(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.listxattr, path)
                os.mkdir(path)
                self.check_dir(os.listxattr, path)

    @unittest.skipIf(not hasattr(os, "lchflags"), "not supported")
    def test_lchflags(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.lchflags, path, stat.UF_APPEND)
                os.mkdir(path)
                self.check_dir(os.lchflags, path, stat.UF_APPEND)

    def test_truncate(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                touch(path)
                self.check_file(os.truncate, path, length=0)

    # def test_readlink(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.readlink(TESTFN)

    # def test_link(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.link(TESTFN, TESTFN2)

    # def test_rename(self, fun=os.rename):
    #     with self.assertRaises(FileNotFoundError):
    #         fun(TESTFN, TESTFN2)
    #     with self.assertRaises(FileNotFoundError):
    #         fun(TESTFN, TESTFN2)

    #     # move file
    #     touch(TESTFN)
    #     fun(TESTFN, TESTFN2)
    #     assert not os.path.exists(TESTFN)
    #     assert os.path.isfile(TESTFN2)
    #     self.tearDown()
    #     # move dir
    #     safe_mkdir(TESTFN)
    #     fun(TESTFN, TESTFN2)
    #     assert not os.path.exists(TESTFN)
    #     assert os.path.isdir(TESTFN2)

    # def test_renames(self):
    #     self.test_rename(fun=os.renames)

    # def test_replace(self):
    #     self.test_rename(fun=os.replace)
