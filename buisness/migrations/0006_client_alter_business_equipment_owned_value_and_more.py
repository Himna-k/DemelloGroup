# Generated by Django 5.1.2 on 2025-04-10 04:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("buisness", "0005_business_secured_loan_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="business",
            name="equipment_owned_value",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="existing_purchase_orders",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="ira_401k_value",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="last_balance",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="market_value_real_estate",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="outstanding_invoices",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="owed_against_real_estate",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="own_residential_real_estate",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="business",
            name="real_estate_secured_note_payment",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="structured_settlement_payment",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "$0"),
                    (2500, "$2,500"),
                    (5000, "$5,000"),
                    (7500, "$7,500"),
                    (10000, "$10,000"),
                    (20000, "$20,000"),
                    (30000, "$30,000"),
                    (40000, "$40,000"),
                    (50000, "$50,000"),
                    (60000, "$60,000"),
                    (70000, "$70,000"),
                    (80000, "$80,000"),
                    (90000, "$90,000"),
                    (100000, "$100,000"),
                    (110000, "$110,000"),
                    (120000, "$120,000"),
                    (130000, "$130,000"),
                    (140000, "$140,000"),
                    (150000, "$150,000"),
                    (160000, "$160,000"),
                    (170000, "$170,000"),
                    (180000, "$180,000"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="business",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="businesses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="businesses",
                to="buisness.client",
            ),
        ),
    ]
