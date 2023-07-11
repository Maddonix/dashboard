import pandas as pd

def match_and_update_ids(product_file, center_product_file):
    # Read the product file
    product_df = pd.read_excel(product_file)

    # Read the center product file
    center_product_df = pd.read_excel(center_product_file)

    # Create a dictionary to store product_name-import_id mappings
    product_dict = {
        row['name']: row['import_id']
        for _, row in product_df.iterrows()
    }

    # Match and update product_import_id in center_product_df
    center_product_df['product_import_id'] = center_product_df['product_name'].map(product_dict)

    # Check for any unmatched product names
    unmatched_products = center_product_df[center_product_df['product_import_id'].isnull()]['product_name']
    if len(unmatched_products) > 0:
        print("Unmatched product names:")
        print(unmatched_products)

    # Save the updated center product file
    center_product_df.to_excel(center_product_file, index=False)
    print(f"Updated {center_product_file} with product_import_id")

    center_product_file = "center_product_with_product_id.xlsx"
    center_product_df.to_excel(center_product_file, index=False)



# Provide the paths to the Excel files
product_file = "product.xlsx"
center_product_file = "center_product.xlsx"

match_and_update_ids(product_file, center_product_file)
