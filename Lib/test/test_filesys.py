"""
Test all filesystem-related modules by using different kind of path types:
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


def safe_rmpath(path):
    try:
        support.unlink(path)
    except IsADirectoryError:
        support.rmtree(path)


def safe_mkdir(path):
    safe_rmpath(path)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def touch(fname):
    with open(fname, "w"):
        pass


class Base(unittest.TestCase):

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


class OSFunctions(Base):

    # def test_access(self):
    #     assert not os.access(TESTFN, os.R_OK)
    #     touch(TESTFN)
    #     assert os.access(TESTFN, os.R_OK)

    def test_chdir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_mkdir(path)
                self.check_dir(os.chdir, path)

    # @unittest.skipIf(not hasattr(os, "chflags"), "not supported")
    # def test_chflags(self):
    #     self.check_file(os.chflags, TESTFN, mode=0o777)
    #     self.check_dir(os.chflags, TESTFN, mode=0o777)

    def test_chmod(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_mkdir(path)
                self.check_dir(os.chmod, path, mode=0o777)
                touch(path)
                self.check_file(os.chmod, path, mode=0o777)

    @unittest.skipIf(not hasattr(os, "chroot"), "not supported")
    @unittest.skipIf(hasattr(os, "getuid") and os.getuid() == 0,
                     "need unprivileged user")
    def test_chroot(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_rmpath(path)  # XXX
                safe_mkdir(path)
                try:
                    self.check_dir(os.chroot, path)
                except PermissionError:
                    pass

    # @unittest.skipIf(not hasattr(os, "lchflags"), "not supported")
    # def test_lchflags(self):
    #     self.check_file(os.lchflags, TESTFN, stat.UF_APPEND)

    # def test_link(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.link(TESTFN, TESTFN2)

    def test_listdir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_mkdir(path)
                self.check_dir(os.listdir, path)
                touch(path)
                self.assertRaises(NotADirectoryError, os.listdir, path)

    def test_scandir(self):
        for path in ALL_PATHS:
            with self.subTest(path=path):
                safe_mkdir(path)
                self.check_dir(lambda p: list(os.scandir(p)), path)
                touch(path)
                self.assertRaises(NotADirectoryError, os.scandir, path)

    # def test_readlink(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.readlink(TESTFN)

    # def test_remove(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.remove(TESTFN)
    #     touch(TESTFN)
    #     os.remove(TESTFN)
    #     assert not os.path.exists(TESTFN)

    # def test_removedirs(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.removedirs(TESTFN)

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

    # def test_rmdir(self):
    #     with self.assertRaises(FileNotFoundError):
    #         os.rmdir(TESTFN)
    #     safe_mkdir(TESTFN)
    #     os.rmdir(TESTFN)
    #     assert not os.path.exists(TESTFN)

    # def test_scandir(self):
    #     with self.assertRaises(FileNotFoundError):
    #         list(os.scandir(TESTFN))
    #     safe_mkdir(TESTFN)
    #     list(os.scandir(TESTFN))

    # def test_stat(self):
    #     self.check_file(os.stat, TESTFN)
    #     self.check_dir(os.stat, TESTFN)

    # @unittest.skipIf(not hasattr(os, "statvs"), "not supported")
    # def test_statvs(self):
    #     self.check_file(os.statvs, TESTFN)
    #     self.check_dir(os.statvs, TESTFN)

    # def test_truncate(self):
    #     self.check_file(os.truncate, TESTFN, 0)
    #     os.remove(TESTFN)
    #     safe_mkdir(TESTFN)
    #     with self.assertRaises(IsADirectoryError):
    #         os.truncate(TESTFN, 0)

    # def test_utime(self):
    #     self.check_file(os.utime, TESTFN)
    #     self.check_dir(os.stat, TESTFN)

    # def test_listxattr(self):
    #     self.check_file(os.listxattr, TESTFN)
    #     self.check_dir(os.listxattr, TESTFN)
