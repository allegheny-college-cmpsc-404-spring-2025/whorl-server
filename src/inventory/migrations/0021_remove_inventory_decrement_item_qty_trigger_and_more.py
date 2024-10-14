# Generated by Django 5.0.6 on 2024-06-18 13:14

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_remove_inventory_decrement_item_qty_trigger_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='inventory',
            name='decrement_item_qty_trigger',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='inventory',
            trigger=pgtrigger.compiler.Trigger(name='decrement_item_qty_trigger', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n            BEGIN\n                IF NEW.item_qty = 0 THEN\n                    DELETE FROM inventory_inventory\n                    WHERE id = OLD.id;\n                ELSE\n                    UPDATE inventory_inventory\n                    SET NEW.item_bulk = NEW.item_qty * item_weight\n                    WHERE id = OLD.id;\n                END IF;\n                RETURN NEW;\n            END;\n        ', hash='04d2b2353d3c8bf6b8cdc123f4b10bd556c05de1', operation='UPDATE', pgid='pgtrigger_decrement_item_qty_trigger_c958b', table='inventory_inventory', when='AFTER')),
        ),
    ]