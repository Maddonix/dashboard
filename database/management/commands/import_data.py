from django.core.management.base import BaseCommand
from ...models import (
    Center, EmissionFactor, Material, Product, ProductGroup, 
    ProductMaterial, ProductWeight, Unit, CenterProduct, ProductEmission,
    EmissionScope, EmissionCause, Resource, EmissionEvaluator
)

from database.calculations import (
    get_product_emission_df,
    save_to_tmp_file,
    create_product_emission_report
)


from ...import_module import (
    import_from_excel, 
    set_remaining_foreign_keys,
    set_reference_product_emission_factor,
    set_center_product_emissions,
    set_center_summary,
    create_product_emission_objects,
    delete_all_data,
    import_all_excel_files,
    create_center_waste_emission_objects,
    create_center_resource_emission_objects,
    create_emission_evaluator_objects
)

class Command(BaseCommand):
    help = 'Imports data from excel files into database'

    def handle(self, *args, **options):
        delete_all_data()
        self.stdout.write(self.style.SUCCESS('All data removed from database'))


        # Assuming that referenced models are imported first
        import_all_excel_files()

        set_remaining_foreign_keys()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        set_reference_product_emission_factor()
        self.stdout.write(self.style.SUCCESS('Reference product emission factor set successfully'))

        set_center_product_emissions()
        self.stdout.write(self.style.SUCCESS('Center product emissions set successfully'))

        set_center_summary()
        self.stdout.write(self.style.SUCCESS('Center summary set successfully'))

        create_product_emission_objects()
        self.stdout.write(self.style.SUCCESS('Product emission objects created successfully'))

        # get a random productemission and print it
        product_emission = ProductEmission.objects.all().first()
        self.stdout.write(self.style.SUCCESS(product_emission))

        # create center waste emission objects
        create_center_waste_emission_objects()
        self.stdout.write(self.style.SUCCESS('Center waste emission objects created successfully'))

        # create center resource emission objects
        create_center_resource_emission_objects()
        self.stdout.write(self.style.SUCCESS('Center resource emission objects created successfully'))

        create_emission_evaluator_objects()
        self.stdout.write(self.style.SUCCESS('Emission evaluator objects created successfully'))

        # test emission evaluator
        evaluator = EmissionEvaluator.objects.all().first()
        evaluator.get_emission_dataframe()
        self.stdout.write(self.style.SUCCESS('Emission evaluator dataframe created successfully'))

        # save to tmp file = 
        product_emission_df = get_product_emission_df()
        save_to_tmp_file(product_emission_df)
        self.stdout.write(self.style.SUCCESS('Product emission dataframe saved to tmp file'))

        # create product emission report
        create_product_emission_report()
        self.stdout.write(self.style.SUCCESS('Product emission report created successfully'))

