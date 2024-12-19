import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bilan',
            fields=[
                ('dateB', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('numE', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nomPrenom', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groupe', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('nomMat', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Conso',
            fields=[
                ('dateC', models.DateField(primary_key=True, serialize=False)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consos', to='home.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='Participe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.conso')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.etudiant')),
            ],
            options={
                'unique_together': {('etudiant', 'conso')},
            },
        ),
        migrations.AddField(
            model_name='conso',
            name='etudiants',
            field=models.ManyToManyField(through='home.Participe', to='home.etudiant'),
        ),
        migrations.CreateModel(
            name='QCM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateQ', models.DateField()),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qcms', to='home.matiere')),
            ],
            options={
                'unique_together': {('dateQ', 'matiere')},
            },
        ),
        migrations.CreateModel(
            name='RepondreBilan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('demande', models.TextField()),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.bilan')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.etudiant')),
            ],
            options={
                'unique_together': {('etudiant', 'bilan')},
            },
        ),
        migrations.CreateModel(
            name='DemandeEn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='home.matiere')),
                ('reponse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matieres', to='home.repondrebilan')),
            ],
        ),
        migrations.AddField(
            model_name='bilan',
            name='etudiants',
            field=models.ManyToManyField(through='home.RepondreBilan', to='home.etudiant'),
        ),
        migrations.CreateModel(
            name='EstNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.DecimalField(decimal_places=2, max_digits=5)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.etudiant')),
                ('qcm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.qcm')),
            ],
            options={
                'unique_together': {('etudiant', 'qcm')},
            },
        ),
    ]
