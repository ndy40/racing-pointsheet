from typing import List, Generic, TypeVar, Iterator
from pydantic import BaseModel

from pointsheet.domain.types import EntityId


T = TypeVar('T')


class PaginationMetadata(BaseModel):
    """Metadata for paginated responses"""
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard response format for paginated data with iteration support"""
    items: List[T]
    pagination: PaginationMetadata

    def __iter__(self) -> Iterator[T]:
        """
        Make the PaginatedResponse iterable.
        This allows using the response directly in a for loop.

        Returns:
            Iterator over the items in the response
        """
        return iter(self.items)

    def __getitem__(self, index):
        """
        Enable indexing to access items directly.

        Args:
            index: The index of the item to retrieve

        Returns:
            The item at the specified index
        """
        return self.items[index]

    def __len__(self):
        """
        Return the number of items in the response.

        Returns:
            The number of items
        """
        return len(self.items)

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """Factory method to create a paginated response"""
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return cls(
            items=items,
            pagination=PaginationMetadata(
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1
            )
        )


class ResourceCreated(BaseModel):
    resource: str | EntityId

class ResourceUpdated(BaseModel):
    resource: str | EntityId