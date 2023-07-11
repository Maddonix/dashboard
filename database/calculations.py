# from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from pandas_profiling import ProfileReport
import os
from django.conf import settings

from database.models import (
    Center,
    EmissionFactor,
    Material,
    Product,
    ProductGroup,
    ProductMaterial,
    ProductEmission
)

def get_center_product_emissions(center: Center) -> List[ProductEmission]:
    """Get all product emissions for a center"""
    return ProductEmission.objects.filter(center_product__center=center)

def get_product_emission_df():
    """Get all product emissions as a pandas DataFrame"""
    queryset = ProductEmission.objects.all().values()
    df = pd.DataFrame.from_records(queryset)
    return df

def save_to_tmp_file(df, file_name="tmp.xlsx"):
    """Save a pandas DataFrame to a temporary file"""
    df.to_excel(file_name, index=False)


def create_product_emission_report(path_only = False):
    df = get_product_emission_df()
    report_file_path = 'frontend/static/product_emission_report.html'

    if path_only:
        return report_file_path

    else: 
        profile = ProfileReport(df, title="Pandas Profiling Report")
        # profile.to_file(report_file_path)
        return report_file_path
