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
    def save_file(
        self, file_path: str, file_content: bytes, rename: bool = False
    ) -> str:
        """Save a file with the given path and content.

        Args:
            file_path: The path where the file should be saved
            file_content: The binary content of the file
            rename: If True, generate a UUID for the filename while preserving extension

        Returns:
            str: The actual path where the file was saved
        """
        import uuid

        allowed_extensions = {"jpeg", "png", "csv", "pdf", "jpg"}
        sanitized_name = secure_filename(file_path)
        extension = os.path.splitext(sanitized_name)[1].lower().lstrip(".")

        if extension not in allowed_extensions:
            raise ValueError(f"File extension '{extension}' is not supported.")

        if rename:
            new_filename = f"{uuid.uuid4()}.{extension}"
            final_path = os.path.join(self.base_path, new_filename)
        else:
            final_path = os.path.join(self.base_path, sanitized_name)

        with open(final_path, "wb") as file:
            file.write(file_content)

        return final_path

    def fetch_file(self, file_path: str) -> bytes:
        """Fetch the content of a file with the given path."""
        full_path = os.path.join(self.base_path, file_path)
        with open(full_path, "rb") as file:
            return file.read()

    def delete_file(self, file_path: str) -> None:
        """Delete a file with the given path."""
        full_path = os.path.join(self.base_path, file_path)
        os.remove(full_path)
