from weakref import ref
from django.shortcuts import render
import pandas as pd

from database.models import CenterResource, CenterProduct, ProductGroup, ProductCatalogue, CenterProducts, Center, TransportStep

def calculate_scope_1():
    # get center resources with resource_import_id in [1,2]
    center_resources = CenterResource.objects.filter(resource__import_id__in=[1,2])
    

    _dicts = []
    # create a list of dictionaries with the years as keys and the emissions as values and a list of the resource names
    for resource in center_resources:
        _dict = {}
        _dict["name"] = resource.name
        _dict["year"] = resource.year
        _dict["emission_kg"] = resource.quantity * resource.use_emission_factor.value
        _dict["quantity"] = resource.quantity
        _dict["unit"] = resource.unit.name
        _dicts.append(_dict)
    
    return _dicts

def calculate_scope_2():
    # get center resources with resource_import_id in [3]
    center_resources = CenterResource.objects.filter(resource__import_id__in=[3])
    
    _dicts = []
    # create a list of dictionaries with the years as keys and the emissions as values and a list of the resource names
    for resource in center_resources:
        _dict = {}
        _dict["name"] = resource.name
        _dict["year"] = resource.year
        _dict["emission_kg"] = resource.quantity * resource.use_emission_factor.value
        _dict["quantity"] = resource.quantity
        _dict["unit"] = resource.unit.name
        _dicts.append(_dict)
    
    return _dicts

def get_product_group_reference_product_emissions(product_group):
    # first we need to fetch the reference product of the product group
    reference_product = product_group.reference_product
    assert reference_product, "Product group has no reference product"

    # now we need to get the ProductMaterial objects pointing to the reference product
    product_materials = reference_product.productmaterial_set.all()

    material_dicts = [
        {   "component": product_material.component,
            "material": product_material.material.name,
            "weight": product_material.weight,
            "emission_factor": product_material.material.emission_factor.value,
        }
        for product_material in product_materials
    ]

    total_weight = 0
    product_weight = 0
    package_weight = 0

    total_emission = 0
    product_emission = 0
    package_emission = 0

    for material_dict in material_dicts:
        if material_dict["component"] == "product":
            product_weight += material_dict["weight"]
            product_emission += material_dict["weight"] * material_dict["emission_factor"]
        elif material_dict["component"] == "package":
            package_weight += material_dict["weight"]
            package_emission += material_dict["weight"] * material_dict["emission_factor"]
        total_weight += material_dict["weight"]
        total_emission += material_dict["weight"] * material_dict["emission_factor"]

    weight_dict = {
        "product": product_weight,
        "package": package_weight,
        "total": total_weight,
    }

    emission_dict = {
        "product": product_emission,
        "package": package_emission,
        "total": total_emission,
    }

    return material_dicts, weight_dict, emission_dict
    

def flatten_ref_prod_emission_dict(data):

# DataFrame 1
    df1_data = {
        "product_group": [],
        "reference_product": [],
        "package_weight_kg": [],
        "product_weight_kg": [],
        "total_weight_kg": [],
        "package_emission_kg": [],
        "product_emission_kg": [],
        "total_emission_kg": [],
    }
    for product_group, details in data.items():
        df1_data["product_group"].append(product_group)
        df1_data["reference_product"].append(details["reference_product"])
        df1_data["package_weight_kg"].append(details["weight"]["package"])
        df1_data["product_weight_kg"].append(details["weight"]["product"])
        df1_data["total_weight_kg"].append(details["weight"]["total"])
        df1_data["package_emission_kg"].append(details["emission_kg"]["package"])
        df1_data["product_emission_kg"].append(details["emission_kg"]["product"])
        df1_data["total_emission_kg"].append(details["emission_kg"]["total"])

    df1 = pd.DataFrame(df1_data)

    # DataFrame 2
    df2_data = {
        "product_group": [],
        "reference_product": [],
        "component": [],
        "emission_factor": [],
        "material": [],
        "weight_kg": [],
    }
    for product_group, details in data.items():
        for material_dict in details["material_dicts"]:
            df2_data["product_group"].append(product_group)
            df2_data["reference_product"].append(details["reference_product"])
            df2_data["component"].append(material_dict["component"])
            df2_data["emission_factor"].append(material_dict["emission_factor"])
            df2_data["material"].append(material_dict["material"])
            df2_data["weight_kg"].append(material_dict["weight"])

    df2 = pd.DataFrame(df2_data)

    return df1, df2


def calculate_scope_3_products():
    # get all groups, for each group get the reference product
    product_groups = ProductGroup.objects.all()

    # get the emissions for each reference product
    emission_dict = {}

    for product_group in product_groups:
        _material_dicts, _weight_dict, _emission_dict = get_product_group_reference_product_emissions(product_group)
        emission_dict[product_group.name] = {
            "reference_product": product_group.reference_product.name,
            "weight": _weight_dict,
            "emission_kg": _emission_dict,
            "material_dicts": _material_dicts,
        }
        
    return emission_dict

import numpy as np
def update_center_products():
    # Get all unique years and products that have an associated product group
    unique_years_and_products = CenterProduct.objects.filter(product__product_group__isnull=False).values('date__year', 'product', 'center').distinct()

    i = 0

    # Iterate over each unique year, product and center
    for item in unique_years_and_products:
        
        # get dictionary of the item
        _dict = dict(item)

        year = item['date__year']
        product = ProductCatalogue.objects.get(pk=item['product'])
        center = Center.objects.get(pk=item['center'])

        # Calculate the total quantity for this year, product and center
        total_quantity = CenterProduct.objects.filter(date__year=year, product=product, center=center).count()

        

        weight_per_product = product.product_weight.get_weight() if product.product_weight else None
        reference_emission_per_weight = product.product_group.get_emission_factor().value
        total_emission = None

        # Check which information is available, exclude if value is None or np.nan:
        has_reference_group = product.product_group is not None
        has_weight_per_product = weight_per_product is not None
        
        
        # has_reference_group = product.product_group is not None
        # has_weight_per_product = weight_per_product is not None

        # If weight_per_product or reference_emission_per_weight does not exist, skip this product
        if not has_reference_group or not has_weight_per_product:
            # print(f"Could not calculate total_emission for {year} and {product.name}")
            continue

        print(f"Calculating total_emission for {year} and {product.name}")

        total_emission = total_quantity * weight_per_product * reference_emission_per_weight

        # Get the existing CenterProducts object or create a new one
        center_products, created = CenterProducts.objects.update_or_create(
            center=center,
            product=product,
            year=year,
            defaults={
                'quantity': total_quantity,
                'weight_per_product': weight_per_product,
                'reference_emission_per_weight': reference_emission_per_weight,
                'total_emission': total_emission,
            }
        )

        print(f"Updated CenterProducts for {year} and {product.name}")

def fetch_center_products():
    # get all CenterProductsObjects by center
    center_products = CenterProducts.objects.all()
    
    # create a dictionary with the center as key and a list of dictionaries as value
    # each dictionary in the list contains the year, product, product_group and total_emission
    center_products_dict = {}
    for center_product in center_products:
        _dict = {
            "center": center_product.center.name,
            "quantity": center_product.quantity,
            "year": center_product.year,
            "product": center_product.product.name,
            "product_group": center_product.product.product_group.name if center_product.product.product_group else None,
            "total_emission_kg": center_product.total_emission,
        }
        if center_product.center.name not in center_products_dict:
            center_products_dict[center_product.center.name] = []
        center_products_dict[center_product.center.name].append(_dict)

    return center_products_dict

def calculate_product_transport_emissions():
    # get all CenterProductsObjects by center
    center_products = CenterProducts.objects.all()
    
    _dicts = []
    for center_product in center_products:
        total_weight = center_product.quantity * center_product.weight_per_product

        # currently we assume that all products have two transport steps (pk == 1 and pk == 2)
        transport_steps_ids = [1,2]
        transport_emission = 0
        for transport_step_id in transport_steps_ids:
            transport_step = TransportStep.objects.get(pk=transport_step_id)
            transport_emission += total_weight * transport_step.emission_factor.value * transport_step.distance

        _dict = {
            "center": center_product.center.name,
            "product": center_product.product.name,
            "total_weight_kg": total_weight,
            "total_emission_kg": transport_emission,
            "year": center_product.year,
        }

        _dicts.append(_dict)

    return _dicts

from database.models import CenterWaste
def calculate_waste_emissions():
    # get all center waste objects
    center_wastes = CenterWaste.objects.all()

    _dicts = []
    for center_waste in center_wastes:
        _dict = {
            "center": center_waste.center.name,
            "waste_type": center_waste.waste.name,
            "weight_kg": center_waste.quantity,
            "year": center_waste.year,
            "emission_kg": center_waste.quantity * center_waste.emission_factor.value,
        }

        _dicts.append(_dict)

    return _dicts

def calculate_resource_transport_emissions():
    # get all CenterResources with resource_import_id in [1,2,3]
    center_resources = CenterResource.objects.filter(resource__import_id__in=[1,2,3])

    _dicts = []
    for center_resource in center_resources:
        quantity = center_resource.quantity
        unit = center_resource.unit.name
        emission_factor = center_resource.transport_emission_factor.value

        _dict = {
            "center": center_resource.center.name,
            "resource": center_resource.resource.name,
            "quantity": quantity,
            "unit": unit,
            "emission_factor": emission_factor,
            "emission_kg": quantity * emission_factor,
            "year": center_resource.year,
        }

        _dicts.append(_dict)
    
    return _dicts

def home(request):
    update_center_products()
    scope_1_records = calculate_scope_1()
    scope_1_records_df = pd.DataFrame(scope_1_records)
    scope_1_records_df_json = scope_1_records_df.to_json(orient='records')

    scope_2_records = calculate_scope_2()
    scope_2_records_df = pd.DataFrame(scope_2_records)
    scope_2_records_df_json = scope_2_records_df.to_json(orient='records')

    center_products = fetch_center_products()
    center_product_material_records = center_products["University Hospital Würzburg"]
    center_product_material_records_df = pd.DataFrame(center_product_material_records)
    center_product_material_records_df_json = center_product_material_records_df.to_json(orient='records')

    product_transport_emissions = calculate_product_transport_emissions()
    product_transport_emissions_df = pd.DataFrame(product_transport_emissions)
    product_transport_emissions_df_json = product_transport_emissions_df.to_json(orient='records')

    waste_emissions = calculate_waste_emissions()
    waste_emissions_df = pd.DataFrame(waste_emissions)
    waste_emissions_df_json = waste_emissions_df.to_json(orient='records')

    resource_transport_emissions = calculate_resource_transport_emissions()
    resource_transport_emissions_df = pd.DataFrame(resource_transport_emissions)
    resource_transport_emissions_df_json = resource_transport_emissions_df.to_json(orient='records')

    # combine dataframes in a new df with the columns scope, year, emission_kg; all dfs have the columns year and emission_kg
    # scope_1_records_df gets value "Scope 1" in the scope column
    # scope_2_records_df gets value "Scope 2" in the scope column
    # center_product_material_records_df gets value "Scope 3 - Products" in the scope column
    # product_transport_emissions_df gets value "Scope 3 - Product Transport" in the scope column
    # waste_emissions_df gets value "Scope 3 - Waste" in the scope column
    # resource_transport_emissions_df gets value "Scope 3 - Resource Transport" in the scope column
     
    # create a list of dataframe / scope_value pairs
    df_scope_pairs = [
        (scope_1_records_df, "Scope 1"),
        (scope_2_records_df, "Scope 2"),
        (center_product_material_records_df, "Scope 3 - Products"),
        (product_transport_emissions_df, "Scope 3 - Product Transport"),
        (waste_emissions_df, "Scope 3 - Waste"),
        (resource_transport_emissions_df, "Scope 3 - Resource Transport"),
    ]

    # create a new dataframe with the columns scope, year, emission_kg
    df = pd.DataFrame(columns=["scope", "year", "emission_kg"])

    # iterate over the list of dataframe / scope_value pairs
    for df_scope_pair in df_scope_pairs:
        # get the dataframe and scope_value
        _df, scope_value = df_scope_pair
        # check if column named "total_emission_kg" exists, if so, rename to emission_kg
        if "total_emission_kg" in _df.columns:
            _df = _df.rename(columns={"total_emission_kg": "emission_kg"})

        # create a record for each year in the dataframe
        # values: scope = scope_value, year = year, emission_kg = sum of all emissions for this year
        _df = _df.groupby("year").sum().reset_index()
        _df["scope"] = scope_value

        # expand df with _df using concat
        df = pd.concat([df, _df], ignore_index=True)

    # drop all columns except scope, year, emission_kg
    df = df[["scope", "year", "emission_kg"]]

    # convert df to json
    summary_df_json = df.to_json(orient='records')

    ######## Ref Product Plot DF ########
    ref_prod_records = calculate_scope_3_products() # returns list of dicts 
    ref_prod_df1, ref_prod_df2 = flatten_ref_prod_emission_dict(ref_prod_records)
    # print(ref_prod_df1)
    ref_prod_df1["emission_per_kg_product"] = ref_prod_df1["total_emission_kg"] / ref_prod_df1["product_weight_kg"]

    # Product Emission plot df 
    # sum up emission for each product group per year from center_product_material_records_df
    # center_product_material_records_df has columns: center, product, product_group, total_emission_kg, year
    # print(center_product_material_records_df)
    plot_product_group_emission_df = center_product_material_records_df.copy()
    plot_product_group_emission_df = plot_product_group_emission_df.loc[:, ["product_group", "year", "total_emission_kg"]]
    plot_product_group_emission_df = plot_product_group_emission_df.groupby(["product_group", "year"]).sum().reset_index()
    plot_product_group_emission_df_json = plot_product_group_emission_df.to_json(orient='records')
    print(plot_product_group_emission_df_json)   
    
    context = {
        "summary": summary_df_json,
        'scope_1': scope_1_records_df_json,
        'scope_2': scope_2_records_df_json,
        "scope_3_reference_products": ref_prod_records,
        "scope_3_center_products": center_product_material_records_df_json,
        "scope_3_product_transport_emissions": product_transport_emissions_df_json,
        "scope_3_waste_emissions": waste_emissions_df_json,
        "scope_3_resource_transport_emissions": resource_transport_emissions_df_json,
        "plot_product_group_emission_df": plot_product_group_emission_df_json,
    }
 

    # convert dataframes to json
    context["ref_prod_df1_json"] = ref_prod_df1.to_json(orient='records')
    context["ref_prod_df2_json"] = ref_prod_df2.to_json(orient='records')



    
    return render(request, 'home.html', context)


