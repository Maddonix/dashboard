from pathlib import Path
import pandas as pd
from django.utils.timezone import make_aware

from database.models import (Unit, Waste, EmissionCause, EmissionFactor, EmissionScope, Manufacturer,
    Resource, ProductWeight, ProductGroup, ProductCatalogue, CenterProduct,
    CenterResource, CenterWaste, TransportStep, Center, Material, ProductMaterial)


DATA_DIR = Path(".../import_data/")
DATA_DIR = DATA_DIR.resolve()

MODEL_LOOKUP = {
    "00-center": Center,
    '01-unit': Unit,
    '02-waste': Waste,
    '03-emission_cause': EmissionCause,
    '04-emission_factor': EmissionFactor,
    '05-emission_scope': EmissionScope,
    '06-manufacturer': Manufacturer,
    '07-resource': Resource,
    '07.5-product_weight': ProductWeight,
    '08-product_group': ProductGroup,
    '09-product_catalogue': ProductCatalogue,
    '10-center_product': CenterProduct,
    '11-center_resource': CenterResource,
    '12-center_waste': CenterWaste,
    '13-transport_step': TransportStep,
    '14-material': Material,
    '15-product_material': ProductMaterial
}

FOREIGN_KEY_FIELDS = {
        "EmissionFactor": ["unit_import_id"],
        "ProductGroup": ["reference_product_import_id"],
        "ProductCatalogue": [
            "product_group_import_id",
            "product_weight_import_id",
            "manufacturer_import_id",
        ],
        "CenterProduct": ["product_import_id", "center_import_id"],
        "CenterResource": [
            "center_import_id",
            "resource_import_id",
            "unit_import_id",
            "use_emission_factor_import_id",
            "transport_emission_factor_import_id",
        ],
        "CenterWaste": [
            "center_import_id",
            "waste_import_id",
            "emission_factor_import_id",
            "unit_import_id"
        ],
        "TransportStep": ["emission_factor_import_id", "unit_import_id"],
        "Material": ["emission_factor_import_id"],
        "ProductMaterial": ["product_import_id", "material_import_id"],
    }

CREATE_OBJECTS_SKIP_FIELDS= {
    "ProductGroup": ["reference_product_import_id"], # is processed in update_product_groups
}


def get_import_data_frames(data_dir = DATA_DIR):
    
    excel_files = list(data_dir.glob("*.xlsx"))

    dfs = {file.stem: pd.read_excel(file) for file in excel_files}

    return dfs

def delete_all_data():
    for model in MODEL_LOOKUP.values():
        model.objects.all().delete()

def create_model_objects(df, Model, skip_fields = None, bulk_size = 1000):

    if not skip_fields:
        skip_fields = CREATE_OBJECTS_SKIP_FIELDS.get(Model.__name__, [])

    # replace all np.NaN and pd.nan values with None
    df = df.where(pd.notnull(df), None)

    bulk_objects = []

    for index, row in df.iterrows():
        instance_data = row.to_dict()

        if "date" in instance_data:
            instance_data["date"] = make_aware(instance_data["date"])

        # If skip_fields is provided, skip these fields
        if skip_fields:
            instance_data = {
                k: v for k, v in instance_data.items() if k not in skip_fields
            }

        # If the model has foreign key fields, rename them and change np.nan to None
        if Model.__name__ in FOREIGN_KEY_FIELDS:
            for fk_field in FOREIGN_KEY_FIELDS[Model.__name__]:
                new_field = fk_field.replace("_import_id", "_id")
                value = instance_data.pop(fk_field, None)

                # If the value is NaN, change it to None
                if pd.isna(value):
                    value = None

                instance_data[new_field] = value


        # Create the Django model instance and add it to the list
        bulk_objects.append(Model(**instance_data))

        if len(bulk_objects) >= bulk_size:
            Model.objects.bulk_create(bulk_objects)
            bulk_objects.clear()

    if bulk_objects:
        Model.objects.bulk_create(bulk_objects)

def update_product_groups(df):
    for index, row in df.iterrows():
        product_group = ProductGroup.objects.get(import_id=row["import_id"])
        reference_product = ProductCatalogue.objects.get(import_id=row["reference_product_import_id"])
        product_group.reference_product = reference_product
        product_group.save()
