from __future__ import annotations
import uuid
from typing import Optional


class BaseEntity:
    def __init__(self) -> None:
        self.id = uuid.uuid4().hex


class Method(BaseEntity):
    def __init__(self, name: str, entity: Entity) -> None:
        super().__init__()
        self.id = uuid.uuid4().hex
        self.name = name
        self.entity = entity


class Entity(BaseEntity):
    def __init__(
            self,
            methods: list[Method],
            sub_entities: list[Entity],
            parent_entity: Optional[Entity],
            is_abstract: bool,
            used_methods: list[Method]
    ) -> None:
        super().__init__()
        self.sub_entities = sub_entities
        self.parent_entity = parent_entity
        self.methods = methods
        self.is_abstract = is_abstract
        self.used_methods = used_methods

    @property
    def is_super(self) -> bool:
        if self.sub_entities:
            return True
        return False

    @property
    def implemented_methods(self) -> list[Method]:
        total_methods = self.methods
        if self.parent_entity:
            total_methods += self.parent_entity.implemented_methods
        return total_methods

    def is_method_used(self, method: Method) -> bool:
        if method in self.used_methods:
            return True
        for sub_class in self.sub_entities:
            is_used = sub_class.is_method_used(method)
            if is_used:
                return True
        return False


class EntitiesHierarchy:
    def __init__(self, entities: list[Entity]) -> None:
        self.entities = entities
