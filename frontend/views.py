from itertools import product
from django.shortcuts import render
from database.models import Center, ProductGroup, EmissionEvaluator
from .ajax_views import get_center_details, get_product_group_details, product_data
# Create your views here.
from database.calculations import get_product_emission_df, create_product_emission_report
from pandas_profiling import ProfileReport
from serializers import ProductGroupSerializer


import json

# PRODUCT_EMISSION_DF = get_product_emission_df()
# PRODUCT_PROFILE = ProfileReport(PRODUCT_EMISSION_DF, title="Pandas Profiling Report")

def dashboard(request):
    product_groups = ProductGroup.objects.all()
    centers = Center.objects.all()

    report_file_path = create_product_emission_report(path_only=True)

    context = {
        "product_groups": product_groups,
        "centers": centers,
        "report_file_path": report_file_path
    }

    return render(request, 'dashboard.html', context)

def about(request):
    return render(request, 'about.html')

def product_groups(request):
    product_groups = ProductGroup.objects.all()

    for group in product_groups:
        group.reference_product.set_materials_string()
    
    # refresh the product groups from the database to get the updated materials string
    product_groups = ProductGroup.objects.all()

    product_group_names = [group.name for group in product_groups]

    # to fetch number of products, we need to get all Product objects which have a foreign key to the ProductGroup object
    # then we can count the number of products for each group

    # product_counts = [group.product_set.count() for group in product_groups]
    product_counts = [group.products.count() for group in product_groups]

    # create serializer instances for each product group, get the data, and convert to a JSON string
    product_group_serializer_data = [ProductGroupSerializer(group).data for group in product_groups]
    product_groups_json = json.dumps(product_group_serializer_data)

    context = {
        'product_group_names': json.dumps(product_group_names),
        'product_counts': json.dumps(product_counts),
        'product_groups': product_groups_json,
        "p_product_groups": product_groups,
    }

    return render(request, 'product_groups.html', context)

def emission_evaluator(request):
    centers = Center.objects.all()

    center=centers.first()
    test_emission_evaluator = EmissionEvaluator.objects.get(center=center)
    # print(f"test_emission_evaluator: {test_emission_evaluator}")
    df = test_emission_evaluator.get_emission_dataframe()
    df_json = df.to_json(orient='records')
    # for col in df.columns:
    #     print(col)

    context = {
        "centers": centers,
        "df": df_json,
    }
    try: 
        df.to_excel("plot_data.xlsx")
    except:
        print("Error saving plot data to excel file")

    return render(request, 'emission_evaluator.html', context)


