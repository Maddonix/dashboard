import pandas as pd
from ..models import (
    Center, 
    EmissionFactor, 
    Material, Product, ProductGroup, ProductMaterial, ProductWeight, Unit, CenterProduct,
    ProductEmission,
    EmissionScope,
    EmissionCause, Resource,
    Waste,
    TransportStep,
    CenterWaste,
    CenterResource,
    Unit,
    WasteEmission,
    ResourceBurntEmission,
    ResourceTransportEmission,
    ElectricityUsedEmission,
    ProductTransportEmission,
    EmissionEvaluator
)

def delete_all_data():
    # pass
    Center.objects.all().delete()
    EmissionFactor.objects.all().delete()
    Material.objects.all().delete()
    Product.objects.all().delete()
    ProductGroup.objects.all().delete()
    ProductMaterial.objects.all().delete()
    ProductWeight.objects.all().delete()
    Unit.objects.all().delete()
    CenterProduct.objects.all().delete()
    ProductEmission.objects.all().delete()
    EmissionScope.objects.all().delete()
    EmissionCause.objects.all().delete()
    Resource.objects.all().delete()
    Waste.objects.all().delete()
    TransportStep.objects.all().delete()
    CenterWaste.objects.all().delete()
    CenterResource.objects.all().delete()
    WasteEmission.objects.all().delete()
    ResourceBurntEmission.objects.all().delete()
    ResourceTransportEmission.objects.all().delete()
    ElectricityUsedEmission.objects.all().delete()
    ProductTransportEmission.objects.all().delete()
    EmissionEvaluator.objects.all().delete()

def import_all_excel_files():
    import_from_excel(r'data/unit.xlsx', Unit)
    import_from_excel(r"data/resource.xlsx", Resource)
    import_from_excel(r'data/emission_factor.xlsx', EmissionFactor)
    import_from_excel(r'data/emission_scope.xlsx', EmissionScope)
    import_from_excel(r'data/emission_cause.xlsx', EmissionCause)
    import_from_excel(r'data/center.xlsx', Center)
    import_from_excel(r'data/material.xlsx', Material)
    import_from_excel(r'data/product_weight.xlsx', ProductWeight)
    import_from_excel(r'data/product_group.xlsx', ProductGroup)
    import_from_excel(r'data/product.xlsx', Product)
    import_from_excel(r'data/product_material.xlsx', ProductMaterial)
    import_from_excel(r'data/center_product_with_product_id.xlsx', CenterProduct)
    import_from_excel(r'data/waste.xlsx', Waste)
    import_from_excel(r"data/center_waste.xlsx", CenterWaste)
    import_from_excel(r"data/center_resource.xlsx", CenterResource)

def set_remaining_foreign_keys():
    # Set remaining foreign keys
    for product in Product.objects.all():
        product.product_group = ProductGroup.objects.get(import_id=product.product_group_import_id)
        product.product_weight = ProductWeight.objects.get(import_id=product.product_weight_import_id)
        product.save()

    for product_material in ProductMaterial.objects.all():
        product_material.product = Product.objects.get(import_id=product_material.product_import_id)
        product_material.material = Material.objects.get(import_id=product_material.material_import_id)
        product_material.save()

    for emission_factor in EmissionFactor.objects.all():
        emission_factor.unit = Unit.objects.get(import_id=emission_factor.unit_import_id)
        emission_factor.save()

    for center_product in CenterProduct.objects.all():
        center_product.center = Center.objects.get(import_id=center_product.center_import_id)
        center_product.product = Product.objects.get(import_id=center_product.product_import_id)
        center_product.save()

    for product_group in ProductGroup.objects.all():
        product_group.reference_product = Product.objects.get(import_id=product_group.reference_product_import_id)
        product_group.save()

def import_from_excel(excel_file, Model):
    df = pd.read_excel(excel_file)
    data = df.to_dict(orient='records')

    if Model == Product:
        # ProductGroup, ProductWeight and EmissionFactor are referenced by Product
        # get correct entry by import_id and add field to dict
        for record in data:
            record['product_group'] = ProductGroup.objects.get(import_id=record['product_group_import_id'])
            record['product_weight'] = ProductWeight.objects.get(import_id=record['product_weight_import_id'])
            

    elif Model == ProductMaterial:
        # Product and Material are referenced by ProductMaterial
        # get correct entry by import_id and add field to dict
        for record in data:
            record['product'] = Product.objects.get(import_id=record['product_import_id'])
            assert record['product']
            record['material'] = Material.objects.get(import_id=record['material_import_id'])

    elif Model == EmissionFactor:
        # Unit is referenced by EmissionFactor
        # get correct entry by import_id and add field to dict
        for record in data:
            record['unit'] = Unit.objects.get(import_id=record['unit_import_id'])

    elif Model == CenterProduct:
        # Center and Product are referenced by CenterProduct
        # get correct entry by import_id and add field to dict
        for record in data:
            record['center'] = Center.objects.get(import_id=record['center_import_id'])
            record['product'] = Product.objects.get(import_id=record['product_import_id'])
            del record["product_name"]

    elif Model == Material:
        # EmissionFactor is referenced by Material
        # get correct entry by import_id and add field to dict
        for record in data:
            record['emission_factor'] = EmissionFactor.objects.get(import_id=record['emission_factor_import_id'])

    elif Model == CenterResource:
        for record in data:
            record["center"] = Center.objects.get(import_id=record["center_import_id"])
            record["resource"] = Resource.objects.get(import_id=record["resource_import_id"])
            record["unit"] = Unit.objects.get(import_id=record["unit_import_id"])
            record["use_emission_factor"] = EmissionFactor.objects.get(import_id=record["use_emission_factor_import_id"])
            record["transport_emission_factor"] = EmissionFactor.objects.get(import_id=record["transport_emission_factor_import_id"])

    elif Model == CenterWaste:
        for record in data:
            record["center"] = Center.objects.get(import_id=record["center_import_id"])
            record["waste"] = Waste.objects.get(import_id=record["waste_import_id"])
            record["emission_factor"] = EmissionFactor.objects.get(import_id=record["emission_factor_import_id"])
            record["unit"] = Unit.objects.get(import_id=record["unit_import_id"])

    elif Model == TransportStep:
        for record in data:
            record["emission_factor"] = EmissionFactor.objects.get(import_id=record["emission_factor_import_id"])
            record["unit"] = Unit.objects.get(import_id=record["unit_import_id"])


    models_instances = []
    for record in data:
        models_instances.append(Model(**record))

    Model.objects.bulk_create(models_instances)

def set_reference_product_emission_factor():
    # get all product_groups
    product_groups = ProductGroup.objects.all()

    # for each product_group
    for product_group in product_groups:
        product_group.set_reference_product_emission_factor()

def create_center_product_transport_emission(center_product:CenterProduct):
    ## TEMPORARILY ALL PRODUCTS GET THE SAME TRANSPORT STEPS
    # get all transport_steps
    transport_steps = TransportStep.objects.all()
    product_quantity = center_product.quantity
    product_weight = center_product.product.product_weight.get_best_weight()
    if not product_weight:
        print(f"no product_weight for {center_product.product.name}")
        product_weight = 0
    if not product_quantity:
        print(f"no product_quantity for {center_product.product.name}")
        product_quantity = 0
    center_product_weight = product_quantity * product_weight

    # for each transport_step
    for transport_step in transport_steps:
        emission = transport_step.emission_factor.value * center_product_weight
        record = {
            "center": center_product.center,
            "product": center_product,
            "transport_step": transport_step,
            "emission": emission,
            "scope": EmissionScope.objects.get(import_id=3),
            "cause": EmissionCause.objects.get(import_id=5),
        }
        ProductTransportEmission.objects.create(**record)

def set_center_product_emissions():
    # get all center_products
    center_products = CenterProduct.objects.all()

    # for each center_product
    for center_product in center_products:
        center_product.calculate_fields()
        create_center_product_transport_emission(center_product)

        # calculate CenterProductTransportEmission

def set_center_summary():
    # get all centers
    centers = Center.objects.all()

    # for each center
    for center in centers:
        center.set_number_product_groups()
        center.set_number_products()
        center.set_total_product_emissions()

def create_center_product_emissions(center:Center):
    # get all center_products
    center_products = CenterProduct.objects.filter(center=center)
    scope = EmissionScope.objects.get(import_id=3)
    cause = EmissionCause.objects.get(import_id=3)
    # for each center_product
    for center_product in center_products:
        record = {
            "center": center,
            "center_name": center.name,
            "product": center_product.product.name,
            "emission": center_product.total_emissions,
            "year": center_product.year,
            "product_weight": center_product.product.product_weight.get_best_weight(),
            "product_quantity": center_product.quantity,
            "emission_per_product": center_product.emissions_per_piece,
            "year": center_product.year,
            "scope": scope,
            "cause": cause,            
        }
        # get or create CenterProductEmission based on center, product and year
        try: 
            center_product_emission, created = ProductEmission.objects.get_or_create(
                center=center,
                product=center_product.product,
                year=center_product.year,
                defaults=record
            )
        except:
            print(record)
            raise Exception("Error while creating CenterProductEmission")
        # if not created, update fields
        if not created:
            for key, value in record.items():
                setattr(center_product_emission, key, value)
            center_product_emission.save()

def create_product_emission_objects():
    # get all centers
    centers = Center.objects.all()

    # for each center
    for center in centers:
        create_center_product_emissions(center)

def create_center_resource_emissions(center:Center):
    # get all center_resources
    center_resources = CenterResource.objects.filter(center=center)

    # if center_resource.resource.import_id in [1,2] calculate use_emission and transport emission
    # if center_resource.resource.import_id in [3] calculate ElectricityEmission

    # for each center_resource
    for center_resource in center_resources:
        if center_resource.resource.import_id in [1,2]:
            # calculate use_emission
            use_emission = center_resource.quantity * center_resource.use_emission_factor.value 
            # create ResourceBurntEmission
            record = {
                "center": center,
                "resource": center_resource,
                "emission": use_emission,
                "year": center_resource.year,
                "scope": EmissionScope.objects.get(import_id=1),
                "cause": EmissionCause.objects.get(import_id=1),
            }
            # create
            ResourceBurntEmission.objects.create(**record)

            # calculate transport_emission
            transport_emission = center_resource.quantity * center_resource.transport_emission_factor.value
            record["emission"] = transport_emission
            record["cause"] = EmissionCause.objects.get(import_id=4)
            record["scope"] = EmissionScope.objects.get(import_id=3)

            # create
            ResourceTransportEmission.objects.create(**record)

        elif center_resource.resource.import_id in [3]:
            # calculate electricity_emission
            electricity_emission = center_resource.quantity * center_resource.use_emission_factor.value
            record = {
                "center": center,
                "resource": center_resource,
                "emission": electricity_emission,
                "year": center_resource.year,
                "scope": EmissionScope.objects.get(import_id=2),
                "cause": EmissionCause.objects.get(import_id=2),
            }
            # create
            ElectricityUsedEmission.objects.create(**record)

            # calculate transport_emission
            transport_emission = center_resource.quantity * center_resource.transport_emission_factor.value
            record["emission"] = transport_emission
            record["cause"] = EmissionCause.objects.get(import_id=4)
            record["scope"] = EmissionScope.objects.get(import_id=3)

            # create
            ResourceTransportEmission.objects.create(**record)



def create_center_resource_emission_objects():
    # get all centers
    centers = Center.objects.all()

    # for each center
    for center in centers:
        create_center_resource_emissions(center)

def create_center_waste_emissions(center:Center):
    # get all center_wastes    
    center_wastes = CenterWaste.objects.filter(center=center)
    scope = EmissionScope.objects.get(import_id=3)
    cause = EmissionCause.objects.get(import_id=6)

    # for each center_waste
    for center_waste in center_wastes:

        # calculate emissions
        quantity = center_waste.quantity
        emission_factor = center_waste.emission_factor.value
        emission = quantity * emission_factor

        record = {
            "center": center,
            "waste": center_waste,
            "emission": emission,
            "year": center_waste.year,
            "scope": scope,
            "cause": cause,
        }

        # get or create CenterWasteEmission based on center, waste and year
        _emission, created = WasteEmission.objects.get_or_create(
            center=center,
            waste=center_waste,
            year=center_waste.year,
            defaults=record
        )
        _emission.save()

def create_center_waste_emission_objects():
    # get all centers
    centers = Center.objects.all()

    # for each center
    for center in centers:
        create_center_waste_emissions(center)

def create_emission_evaluator(center:Center):
    # get all center_emissions
    product_emissions = ProductEmission.objects.filter(center=center).all()
    product_transport_emissions = ProductTransportEmission.objects.filter(center=center)
    resource_burnt_emissions = ResourceBurntEmission.objects.filter(center=center)
    resource_transport_emissions = ResourceTransportEmission.objects.filter(center=center)
    waste_emissions = WasteEmission.objects.filter(center=center)
    electricity_used_emissions = ElectricityUsedEmission.objects.filter(center=center)

    # create an evaluator instance first
    evaluator = EmissionEvaluator.objects.create(center=center)

    # then assign many-to-many related objects
    evaluator.product_emissions.set(product_emissions)
    evaluator.product_transport_emissions.set(product_transport_emissions)
    evaluator.resource_burnt_emissions.set(resource_burnt_emissions)
    evaluator.resource_transport_emissions.set(resource_transport_emissions)
    evaluator.waste_emissions.set(waste_emissions)
    evaluator.electricity_used_emissions.set(electricity_used_emissions)


def create_emission_evaluator_objects():
    # get all centers
    centers = Center.objects.all()

    # for each center
    for center in centers:
        create_emission_evaluator(center)

