"""File to specify the Backpack class."""

import pickle

class Backpack:
    def __init__(self, name="Backpack", capacity=5):
        self.name = name
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
        else:
            raise Exception("Backpack is full")

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
