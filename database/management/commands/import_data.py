from django.core.management.base import BaseCommand
from ...utils import get_import_data_frames, create_model_objects, MODEL_LOOKUP, update_product_groups

class Command(BaseCommand):
    help = 'IMport all data from /import_data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start Import'))
        dfs = get_import_data_frames()

        for df_name, df in dfs.items():
            self.stdout.write(self.style.SUCCESS(f'Importing {df_name}'))
            
            # FIXME: Still necessary?
            _df = df.copy()
            model = MODEL_LOOKUP[df_name]

            create_model_objects(_df, model)

            ######## FIXME: Still necessary?
            # if "import_id" in _df.columns:
            #     _df = _df.dropna(subset=["import_id"])


        self.stdout.write(self.style.SUCCESS('Import successful'))
        self.stdout.write(self.style.SUCCESS('Start updating product groups'))

        update_product_groups(
            dfs["08-product_group"]
        )



