import os
import unittest
from psutil.tests import TestMemoryLeak


class TestOs(TestMemoryLeak):

    @unittest.skipIf(not hasattr(os, "ctermid"), "not available")
    def test_ctermid(self):
        self.execute(os.ctermid)

    def test_environ(self):
        self.execute(lambda: os.environ)

    def test_environb(self):
        self.execute(lambda: os.environb)

    def test_chdir(self):
        here = os.getcwd()
        self.execute(lambda: os.chdir(here))

    def test_fchdir(self):
        fd = os.open(".", os.O_RDONLY)
        self.addCleanup(os.close, fd)
        self.execute(lambda: os.fchdir(fd))

    def test_getcwd(self):
        self.execute(os.getcwd)

    def test_fsencode(self):
        self.execute(lambda: os.fsencode(__file__))

    def test_fsdecode(self):
        self.execute(lambda: os.fsdecode(__file__))

    def test_fspath(self):
        self.execute(lambda: os.fspath(__file__))

    def test_getenv(self):
        self.execute(lambda: os.getenv('foo'))

    def test_getenvb(self):
        self.execute(lambda: os.getenvb(b'foo'))

    def test_get_exec_path(self):
        self.execute(lambda: os.get_exec_path())

    def test_getegid(self):
        self.execute(lambda: os.getegid())

    def test_confstr(self):
        self.execute(lambda: os.confstr('CS_GNU_LIBC_VERSION'))

    def test_listxttrs(self):
        self.execute(lambda: os.listxattr(__file__))


if __name__ == "__main__":
    unittest.main(verbosity=2)
