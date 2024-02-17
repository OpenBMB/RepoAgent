import fnmatch
import os


class GitignoreChecker:
    def __init__(self, directory: str, gitignore_path: str):
        """
        Initialize the GitignoreChecker with a specific directory and the path to a .gitignore file.

        Args:
            directory (str): The directory to be checked.
            gitignore_path (str): The path to the .gitignore file.
        """
        self.directory = directory
        self.gitignore_path = gitignore_path
        self.folder_patterns, self.file_patterns = self._load_gitignore_patterns()

    def _load_gitignore_patterns(self) -> tuple:
        """
        Load and parse the .gitignore file, then split the patterns into folder and file patterns.

        If the specified .gitignore file is not found, fall back to the default path.

        Returns:
            tuple: A tuple containing two lists - one for folder patterns and one for file patterns.
        """
        try:
            with open(self.gitignore_path, "r", encoding="utf-8") as file:
                gitignore_content = file.read()
        except FileNotFoundError:
            # Fallback to the default .gitignore path if the specified file is not found
            default_path = os.path.join(
                os.path.dirname(__file__), "..", "..", ".gitignore"
            )
            with open(default_path, "r", encoding="utf-8") as file:
                gitignore_content = file.read()

        patterns = self._parse_gitignore(gitignore_content)
        return self._split_gitignore_patterns(patterns)

    @staticmethod
    def _parse_gitignore(gitignore_content: str) -> list:
        """
        Parse the .gitignore content and return patterns as a list.

        Args:
            gitignore_content (str): The content of the .gitignore file.

        Returns:
            list: A list of patterns extracted from the .gitignore content.
        """
        patterns = []
        for line in gitignore_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
        return patterns

    @staticmethod
    def _split_gitignore_patterns(gitignore_patterns: list) -> tuple:
        """
        Split the .gitignore patterns into folder patterns and file patterns.

        Args:
            gitignore_patterns (list): A list of patterns from the .gitignore file.

        Returns:
            tuple: Two lists, one for folder patterns and one for file patterns.
        """
        folder_patterns = []
        file_patterns = []
        for pattern in gitignore_patterns:
            if pattern.endswith("/"):
                folder_patterns.append(pattern.rstrip("/"))
            else:
                file_patterns.append(pattern)
        return folder_patterns, file_patterns

    @staticmethod
    def _is_ignored(path: str, patterns: list, is_dir: bool = False) -> bool:
        """
        Check if the given path matches any of the patterns.

        Args:
            path (str): The path to check.
            patterns (list): A list of patterns to check against.
            is_dir (bool): True if the path is a directory, False otherwise.

        Returns:
            bool: True if the path matches any pattern, False otherwise.
        """
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
            if is_dir and pattern.endswith("/") and fnmatch.fnmatch(path, pattern[:-1]):
                return True
        return False

    def check_files_and_folders(self) -> list:
        """
        Check all files and folders in the given directory against the split gitignore patterns.
        Return a list of files that are not ignored and have the '.py' extension.
        The returned file paths are relative to the self.directory.

        Returns:
            list: A list of paths to files that are not ignored and have the '.py' extension.
        """
        not_ignored_files = []
        for root, dirs, files in os.walk(self.directory):
            dirs[:] = [
                d
                for d in dirs
                if not self._is_ignored(d, self.folder_patterns, is_dir=True)
            ]

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.directory)
                if not self._is_ignored(
                    file, self.file_patterns
                ) and file_path.endswith(".py"):
                    not_ignored_files.append(relative_path)

        return not_ignored_files


# Example usage:
# gitignore_checker = GitignoreChecker('path_to_directory', 'path_to_gitignore_file')
# not_ignored_files = gitignore_checker.check_files_and_folders()
# print(not_ignored_files)
