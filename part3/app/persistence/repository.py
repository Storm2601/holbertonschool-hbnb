#!/usr/bin/python3

"""In-memory repository interface and implementation."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repository."""

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Get an object by ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Get all objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by attribute."""
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface."""

    def __init__(self):
        """Initialize an empty storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """Add an object to the storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with new data."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object from storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute."""
        return next((obj for obj in self._storage.values()
                     if getattr(obj, attr_name) == attr_value), None)