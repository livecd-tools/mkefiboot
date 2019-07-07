#
# Copyright (C) 2018 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
from subprocess import CalledProcessError
import tempfile
import unittest

from pymkefiboot.executils import startProgram
from pymkefiboot.executils import execWithRedirect, execWithCapture, execReadlines
from pymkefiboot.executils import runcmd, runcmd_output, setenv

class ExecUtilsTest(unittest.TestCase):
    def startProgram_test(self):
        cmd = ["python3", "-c", "import os; print(os.environ['LC_ALL'])"]
        proc = startProgram(cmd, reset_lang=True)
        (stdout, _stderr) = proc.communicate()
        self.assertEqual(stdout.strip(), b"C")

        cmd = ["python3", "-c", "import os; print(os.environ['LORAX_TEST'])"]
        proc = startProgram(cmd, env_add={"LORAX_TEST": "beefy miracle"})
        (stdout, _stderr) = proc.communicate()
        self.assertEqual(stdout.strip(), b"beefy miracle")

        cmd = ["python3", "-c", "import os; print('HOME' in os.environ)"]
        proc = startProgram(cmd, env_prune=["HOME"])
        (stdout, _stderr) = proc.communicate()
        self.assertEqual(stdout.strip(), b"False")

    def childenv_test(self):
        """Test setting a child environmental variable"""
        setenv("LORAX_CHILD_TEST", "mustard IS progress")
        cmd = ["python3", "-c", "import os; print(os.environ['LORAX_CHILD_TEST'])"]

        proc = startProgram(cmd)
        (stdout, _stderr) = proc.communicate()
        self.assertEqual(stdout.strip(), b"mustard IS progress")

    def execWithRedirect_test(self):
        import logging
        logger = logging.getLogger("pymkefiboot")
        logger.addHandler(logging.NullHandler())
        program_log = logging.getLogger("program")
        program_log.setLevel(logging.INFO)

        tmp_f = tempfile.NamedTemporaryFile(delete=False)
        fh = logging.FileHandler(filename=tmp_f.name, mode="w")
        program_log.addHandler(fh)

        try:
            cmd = ["python3", "-c", "import sys; print('The Once-ler was here.'); sys.exit(1)"]
            rc = execWithRedirect(cmd[0], cmd[1:])
            self.assertEqual(rc, 1)

            tmp_f.file.close()
            logged_text = open(tmp_f.name, "r").readlines()[-1].strip()
            self.assertEqual(logged_text, "The Once-ler was here.")
        finally:
            os.unlink(tmp_f.name)
            program_log.removeHandler(fh)

    def execWithCapture_test(self):
        cmd = ["python3", "-c", "import sys; print('Truffula trees.', end=''); sys.exit(0)"]
        stdout = execWithCapture(cmd[0], cmd[1:], callback=lambda p: True)
        self.assertEqual(stdout.strip(), "Truffula trees.")

    def returncode_test(self):
        cmd = ["python3", "-c", "import sys; print('Truffula trees.'); sys.exit(1)"]
        with self.assertRaises(CalledProcessError):
            execWithCapture(cmd[0], cmd[1:], raise_err=True)

    def exec_filter_stderr_test(self):
        cmd = ["python3", "-c", "import sys; print('Truffula trees.', file=sys.stderr); sys.exit(0)"]
        stdout = execWithCapture(cmd[0], cmd[1:], filter_stderr=True)
        self.assertEqual(stdout.strip(), "")

    def execReadlines_test(self):
        cmd = ["python3", "-c", "import sys; print('Truffula trees.'); sys.exit(0)"]
        iterator = execReadlines(cmd[0], cmd[1:], callback=lambda p: True, filter_stderr=True)
        self.assertEqual(list(iterator), ["Truffula trees."])

    def execReadlines_error_test(self):
        with self.assertRaises(OSError):
            execReadlines("foo-prog", [])

    def del_execReadlines_test(self):
        cmd = ["python3", "-c", "import sys; print('Truffula trees.'); sys.exit(0)"]
        iterator = execReadlines(cmd[0], cmd[1:], callback=lambda p: True)
        del iterator

    def runcmd_test(self):
        cmd = ["python3", "-c", "import sys; print('Theodor Seuss Geisel'); sys.exit(0)"]
        rc = runcmd(cmd)
        self.assertEqual(rc, 0)

    def runcmd_output_test(self):
        cmd = ["python3", "-c", "import sys; print('Everyone needs Thneeds'); sys.exit(0)"]
        stdout = runcmd_output(cmd)
        self.assertEqual(stdout.strip(), "Everyone needs Thneeds")

    def chroot_test(self):
        """Test the preexec function"""
        cmd = ["python3", "-c", "import sys; print('Failure is always an option'); sys.exit(0)"]

        # There is no python3 in /tmp so this is expected to fail
        with self.assertRaises(FileNotFoundError):
            startProgram(cmd, root="/tmp/")

    def preexec_test(self):
        """Test the preexec function"""
        cmd = ["python3", "-c", "import sys; print('Failure is always an option'); sys.exit(0)"]

        # There is no python3 in /tmp so this is expected to fail
        proc = startProgram(cmd, reset_handlers=True, preexec_fn=lambda: True)
        (stdout, _stderr) = proc.communicate()
        self.assertEqual(stdout.strip(), b"Failure is always an option")
