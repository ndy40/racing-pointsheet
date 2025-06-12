import abc
import os
from werkzeug.utils import secure_filename

# Note: boto3 needs to be added as a dependency in pyproject.toml
# [tool.poetry.dependencies]
# boto3 = "^1.34.0"
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    pass  # boto3 will be required only when using S3FileStore


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

        allowed_extensions = {"jpeg", "png", "csv", "pdf", "jpg", "webp"}
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


class S3FileStore(FileStore):
    """Implementation of FileStore for AWS S3."""

    def __init__(
        self,
        bucket_name: str,
        base_path: str = "",
        region_name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
    ):
        """Initialize S3FileStore.

        Args:
            bucket_name: The name of the S3 bucket
            base_path: The base path within the bucket (optional)
            region_name: AWS region name (optional)
            aws_access_key_id: AWS access key ID (optional)
            aws_secret_access_key: AWS secret access key (optional)
        """
        super().__init__(base_path)
        self.bucket_name = bucket_name

        # Initialize S3 client
        session_kwargs = {}
        if region_name:
            session_kwargs["region_name"] = region_name
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key

        self.s3_client = boto3.client("s3", **session_kwargs)

    def save_file(
        self, file_path: str, file_content: bytes, rename: bool = False
    ) -> str:
        """Save a file to S3 bucket.

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
            s3_key = (
                os.path.join(self.base_path, new_filename)
                if self.base_path
                else new_filename
            )
        else:
            s3_key = (
                os.path.join(self.base_path, sanitized_name)
                if self.base_path
                else sanitized_name
            )

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=self._get_content_type(extension),
            )
            return s3_key
        except ClientError as e:
            raise RuntimeError(f"Failed to upload file to S3: {str(e)}")

    def fetch_file(self, file_path: str) -> bytes:
        """Fetch the content of a file from S3 bucket.

        Args:
            file_path: The path of the file to fetch

        Returns:
            bytes: The binary content of the file
        """
        s3_key = (
            os.path.join(self.base_path, file_path) if self.base_path else file_path
        )

        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found in S3: {file_path}")
            raise RuntimeError(f"Failed to fetch file from S3: {str(e)}")

    def delete_file(self, file_path: str) -> None:
        """Delete a file from S3 bucket.

        Args:
            file_path: The path of the file to delete
        """
        s3_key = (
            os.path.join(self.base_path, file_path) if self.base_path else file_path
        )

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            raise RuntimeError(f"Failed to delete file from S3: {str(e)}")

    def _get_content_type(self, extension: str) -> str:
        """Get the MIME type for a file extension.

        Args:
            extension: The file extension

        Returns:
            str: The MIME type
        """
        content_types = {
            "jpeg": "image/jpeg",
            "jpg": "image/jpeg",
            "png": "image/png",
            "csv": "text/csv",
            "pdf": "application/pdf",
        }
        return content_types.get(extension, "application/octet-stream")
