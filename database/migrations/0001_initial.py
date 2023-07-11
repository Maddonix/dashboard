# Generated by Django 4.2.2 on 2023-07-10 22:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('total_product_emissions', models.FloatField(blank=True, null=True)),
                ('number_product_groups', models.IntegerField(blank=True, null=True)),
                ('number_products', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='CenterProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('price_per_piece', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('center_import_id', models.IntegerField(blank=True, null=True)),
                ('product_import_id', models.IntegerField(blank=True, null=True)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('total_emissions', models.FloatField(blank=True, null=True)),
                ('emissions_per_piece', models.FloatField(blank=True, null=True)),
                ('emissions_per_kg', models.FloatField(blank=True, null=True)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_products', to='database.center')),
            ],
        ),
        migrations.CreateModel(
            name='CenterResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='amount')),
                ('year', models.IntegerField()),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_resources', to='database.center')),
            ],
        ),
        migrations.CreateModel(
            name='EmissionCause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EmissionFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('value', models.FloatField()),
                ('unit_import_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmissionScope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('name_german', models.CharField(max_length=255)),
                ('emission_factor_import_id', models.IntegerField(blank=True, null=True)),
                ('emission_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='database.emissionfactor')),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('product_group_import_id', models.IntegerField(blank=True, null=True)),
                ('product_weight_import_id', models.IntegerField(blank=True, null=True)),
                ('materials_str', models.CharField(blank=True, max_length=255, null=True)),
                ('emission_factor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='database.emissionfactor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransportEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transport_emissions', to='database.center')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transport_emissions', to='database.centerproduct')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
            ],
            options={
                'unique_together': {('center', 'product', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Waste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='TransportStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('emission_factor_import_id', models.IntegerField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('unit_import_id', models.IntegerField(blank=True, null=True)),
                ('emission_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_steps', to='database.emissionfactor')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.unit')),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='ResourceTransportEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_transport_emissions', to='database.center')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_emissions', to='database.centerresource')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceBurntEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='burnt_emissions', to='database.center')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='burnt_emissions', to='database.centerresource')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='ProductWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('measured', models.FloatField(blank=True, null=True)),
                ('verified', models.FloatField(blank=True, null=True)),
                ('manufacturer', models.FloatField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('reference_product_import_id', models.IntegerField(blank=True, null=True)),
                ('reference_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.product')),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='database.productgroup'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_weight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.productweight'),
        ),
        migrations.AddField(
            model_name='emissionfactor',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.unit'),
        ),
        migrations.CreateModel(
            name='ElectricityUsedEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electricity_used_emissions', to='database.center')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electricity_used_emissions', to='database.centerresource')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CenterWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='amount')),
                ('year', models.IntegerField()),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_wastes', to='database.center')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_wastes', to='database.unit')),
                ('waste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_wastes', to='database.waste')),
            ],
        ),
        migrations.AddField(
            model_name='centerresource',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_resources', to='database.resource'),
        ),
        migrations.AddField(
            model_name='centerresource',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_resources', to='database.unit'),
        ),
        migrations.AddField(
            model_name='centerproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_products', to='database.product'),
        ),
        migrations.CreateModel(
            name='WasteEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_emissions', to='database.center')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
                ('waste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_emissions', to='database.centerwaste')),
            ],
            options={
                'unique_together': {('center', 'waste', 'year')},
            },
        ),
        migrations.CreateModel(
            name='ProductTransportStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('product_import_id', models.IntegerField(blank=True, null=True)),
                ('transport_step_import_id', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_steps', to='database.product')),
                ('product_transport_emission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_transport_steps', to='database.producttransportemission')),
                ('transport_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='database.transportstep')),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='ProductMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('import_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('weight_g', models.FloatField()),
                ('product_import_id', models.IntegerField(blank=True, null=True)),
                ('material_import_id', models.IntegerField(blank=True, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='database.material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='database.product')),
            ],
            options={
                'unique_together': {('import_datetime', 'import_id')},
            },
        ),
        migrations.CreateModel(
            name='ProductEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission', models.FloatField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('center_name', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('product_quantity', models.FloatField(blank=True, null=True)),
                ('product_weight', models.FloatField(blank=True, null=True)),
                ('emission_per_product', models.FloatField(blank=True, null=True)),
                ('cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissioncause')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_emissions', to='database.center')),
                ('scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.emissionscope')),
            ],
            options={
                'unique_together': {('center', 'product', 'year')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('import_datetime', 'import_id')},
        ),
        migrations.AlterUniqueTogether(
            name='emissionfactor',
            unique_together={('import_datetime', 'import_id')},
        ),
        migrations.AlterUniqueTogether(
            name='centerproduct',
            unique_together={('import_datetime', 'import_id')},
        ),
    ]