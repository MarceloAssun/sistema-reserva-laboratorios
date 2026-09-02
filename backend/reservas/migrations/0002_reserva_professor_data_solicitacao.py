from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("reservas", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="reserva",
            name="data_solicitacao",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reserva",
            name="professor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reservas",
                null=True,
                blank=True,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="reserva",
            name="laboratorio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reservas",
                to="laboratorios.laboratorio",
            ),
        ),
        migrations.AlterField(
            model_name="reserva",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDENTE", "Pendente"),
                    ("APROVADA", "Aprovada"),
                    ("REJEITADA", "Rejeitada"),
                    ("CANCELADA", "Cancelada"),
                ],
                default="PENDENTE",
                max_length=20,
            ),
        ),
    ]
