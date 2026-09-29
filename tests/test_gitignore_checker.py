import os
import tempfile
import unittest

from repo_agent.utils.gitignore_checker import GitignoreChecker


class TestGitignoreChecker(unittest.TestCase):
    def test_a_path_pattern_ignores_that_file(self):
        with tempfile.TemporaryDirectory() as directory:
            hidden = os.path.join(directory, "hidden")
            os.makedirs(hidden)
            with open(os.path.join(hidden, "secret.py"), "w", encoding="utf-8") as handle:
                handle.write("secret = 1\n")
            with open(os.path.join(directory, "keep.py"), "w", encoding="utf-8") as handle:
                handle.write("keep = 1\n")
            gitignore = os.path.join(directory, ".gitignore")
            with open(gitignore, "w", encoding="utf-8") as handle:
                handle.write("hidden/secret.py\n")

            found = GitignoreChecker(directory, gitignore).check_files_and_folders()

        self.assertEqual(sorted(found), ["keep.py"])

    def test_a_basename_pattern_still_ignores_that_file(self):
        with tempfile.TemporaryDirectory() as directory:
            hidden = os.path.join(directory, "hidden")
            os.makedirs(hidden)
            with open(os.path.join(hidden, "secret.py"), "w", encoding="utf-8") as handle:
                handle.write("secret = 1\n")
            with open(os.path.join(directory, "keep.py"), "w", encoding="utf-8") as handle:
                handle.write("keep = 1\n")
            gitignore = os.path.join(directory, ".gitignore")
            with open(gitignore, "w", encoding="utf-8") as handle:
                handle.write("secret.py\n")

            found = GitignoreChecker(directory, gitignore).check_files_and_folders()

        self.assertEqual(sorted(found), ["keep.py"])


if __name__ == "__main__":
    unittest.main()
