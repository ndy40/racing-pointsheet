from typing import Any

import lagom.exceptions
from lagom import Container
from lato import DependencyProvider
from lato.types import DependencyIdentifier


class LagomDependencyProvider(DependencyProvider):
    allow_names = False

    def __init__(self, lagom_container: Container):
        self.container = lagom_container

    def has_dependency(self, identifier: str | type) -> bool:
        if identifier is str:
            return False

        return identifier in self.container.defined_types

    def register_dependency(self, identifier: DependencyIdentifier, dependency: Any):
        if identifier is str:
            raise ValueError(
                f"Lagom container does not support string identifiers: {identifier}"
            )

        try:
            self.container[identifier] = dependency
        except lagom.exceptions.DuplicateDefinition:
            pass

    def get_dependency(self, identifier: DependencyIdentifier) -> Any:
        if identifier is str:
            raise ValueError(
                f"Lagom container does not support string identifiers: {identifier}"
            )
        return self.container.resolve(identifier)

    def copy(self, *args, **kwargs) -> DependencyProvider:
        dp = LagomDependencyProvider(self.container.clone())
        dp.update(*args, **kwargs)
        return dp
