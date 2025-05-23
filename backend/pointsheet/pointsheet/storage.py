import abc
import os
from werkzeug.utils import secure_filename


class FileStore(abc.ABC):
    def __init__(self, base_path: str):
        self.base_path = base_path

    @abc.abstractmethod
    def save_file(self, file_path: str, file_content: bytes) -> None:
        """Save a file with the given path and content."""
        pass

    @abc.abstractmethod
    def fetch_file(self, file_path: str) -> bytes:
        """Fetch the content of a file with the given path."""
        pass

    @abc.abstractmethod
    def delete_file(self, file_path: str) -> None:
        """Delete a file with the given path."""
        pass


class LocalFileStore(FileStore):
    def save_file(self, file_path: str, file_content: bytes) -> None:
        """Save a file with the given path and content."""
        allowed_extensions = {"jpeg", "png", "csv", "pdf", "jpg"}
        sanitized_name = secure_filename(file_path)
        extension = os.path.splitext(sanitized_name)[1].lower().lstrip(".")
        if extension not in allowed_extensions:
            raise ValueError(f"File extension '{extension}' is not supported.")

        with open(file_path, "wb") as file:
            file.write(file_content)

        return file_path

    def fetch_file(self, file_path: str) -> bytes:
        """Fetch the content of a file with the given path."""
        full_path = os.path.join(self.base_path, file_path)
        with open(full_path, "rb") as file:
            return file.read()

    def delete_file(self, file_path: str) -> None:
        """Delete a file with the given path."""
        full_path = os.path.join(self.base_path, file_path)
        os.remove(full_path)
