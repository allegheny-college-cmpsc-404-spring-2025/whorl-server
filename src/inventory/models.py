import pgtrigger
import pickle
from django.db import models
from .backpack import Backpack

@pgtrigger.register(
    pgtrigger.Trigger(
        name='decrement_item_qty_trigger',
        level=pgtrigger.Row,
        operation=pgtrigger.Update,
        when=pgtrigger.After,
        func="""
            BEGIN
                IF NEW.item_qty <= 0 THEN
                    DELETE FROM inventory_inventory
                    WHERE id = OLD.id;
                END IF;
                RETURN NEW;
            END;
        """
    ),
    pgtrigger.Trigger(
        name='detect_inventory_overburden',
        level=pgtrigger.Row,
        operation=pgtrigger.Update,
        when=pgtrigger.After,
        func="""
            DECLARE
                volume int;
            BEGIN
                volume := NEW.item_weight + (SELECT SUM(item_bulk) FROM inventory_inventory WHERE item_owner_id = NEW.item_owner_id);
                IF volume > 11 THEN
                    RAISE EXCEPTION 'overburdened';
                END IF;
                RETURN NEW;
            END;
        """
    )
)
class Inventory(models.Model):
    item_owner = models.ForeignKey(
        'omnipresence.OmnipresenceModel',
        on_delete=models.DO_NOTHING,
        default=0
    )
    item_name = models.CharField(max_length=255)
    item_qty = models.FloatField(default=1.0)
    item_weight = models.FloatField(default=1.0)
    item_bulk = models.FloatField(default=1.0)
    item_version = models.CharField(max_length=255, default="1.0.0")
    item_consumable = models.BooleanField(default=False)
    item_bytestring = models.BinaryField(default=b'\x08', editable=True)

    def __str__(self):
        return self.item_name

    def as_dict(self):
        result = {}
        fields = self._meta.fields
        for field in fields:
            result[field.name] = getattr(self, field.name)
        return result

    def is_container(self):
        """Check if the item is a container (e.g., Backpack)."""
        return self.item_name.lower() == "backpack"

    def get_container_items(self):
        """Retrieve items contained in the container."""
        if self.is_container():
            return Backpack.deserialize(self.item_bytestring).items
        return []

    def add_to_container(self, item):
        """Add an item to the container."""
        if self.is_container():
            backpack = Backpack.deserialize(self.item_bytestring)
            backpack.add_item(item)
            self.item_bytestring = backpack.serialize()
            self.save()
