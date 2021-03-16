# Generated by Django 3.0.6 on 2021-03-16 05:36

from django.db import migrations, models
import django.db.models.deletion
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20210312_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('dest_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('dest_name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('temprature', models.FloatField()),
                ('humidity', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(max_length=200)),
                ('type_of_room', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('stayCharge_dayPerRoom', models.FloatField()),
                ('mealCharge_perPerson', models.FloatField()),
                ('capacity', models.IntegerField()),
                ('service', models.CharField(max_length=200)),
                ('rate_hotel', models.FloatField()),
                ('image_hotel', models.ImageField(height_field=500, upload_to='', width_field=500)),
                ('type_of_hotel', models.CharField(max_length=200)),
                ('dest_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('place_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('name_place', models.CharField(max_length=100)),
                ('desc_place', models.CharField(max_length=400)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('extra_charge', models.FloatField()),
                ('time_durationForVisit', models.TimeField()),
                ('rate_place', models.FloatField()),
                ('type_of_Place', models.CharField(choices=[(travel.models.placeTypeChoice['beach'], 'beach'), (travel.models.placeTypeChoice['shopping'], 'shopping'), (travel.models.placeTypeChoice['historical'], 'historical'), (travel.models.placeTypeChoice['tracking'], 'tracking'), (travel.models.placeTypeChoice['religious'], 'religious'), (travel.models.placeTypeChoice['relaxing'], 'relaxing')], max_length=15)),
                ('dest_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('trans_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('driver_name', models.CharField(max_length=100)),
                ('trans_contact', models.IntegerField()),
                ('capacity_trans', models.IntegerField()),
                ('charge_per_person', models.FloatField()),
                ('place_hold_once_sd', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Destination')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='User_Input',
            fields=[
                ('trip_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField()),
                ('no_of_adult', models.IntegerField()),
                ('no_of_child', models.IntegerField()),
                ('budget', models.CharField(max_length=10)),
                ('visit_place_type', models.CharField(choices=[(travel.models.placeTypeChoice['beach'], 'beach'), (travel.models.placeTypeChoice['shopping'], 'shopping'), (travel.models.placeTypeChoice['historical'], 'historical'), (travel.models.placeTypeChoice['tracking'], 'tracking'), (travel.models.placeTypeChoice['religious'], 'religious'), (travel.models.placeTypeChoice['relaxing'], 'relaxing')], max_length=15)),
                ('trans_to_choose', models.CharField(max_length=10)),
                ('dest_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Destination')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User')),
            ],
        ),
        migrations.CreateModel(
            name='User_Account',
            fields=[
                ('account_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('acount_balance', models.FloatField()),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User')),
            ],
        ),
        migrations.CreateModel(
            name='Transport_Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ofBooking_trans', models.DateField()),
                ('start_dateOfTrans', models.DateField()),
                ('end_dateOfTrans', models.DateField()),
                ('source', models.CharField(max_length=200)),
                ('type_of_trans', models.CharField(max_length=10)),
                ('no_of_person_onTrans', models.IntegerField()),
                ('charge_of_trans', models.FloatField()),
                ('trans_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Transport')),
                ('trip_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User_Input')),
            ],
            options={
                'unique_together': {('trans_id', 'trip_id')},
            },
        ),
        migrations.CreateModel(
            name='Taxi_Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ofBooking_taxi', models.DateField()),
                ('charge_ofTaxiRide', models.FloatField()),
                ('trans_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Transport')),
                ('trip_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User_Input')),
            ],
            options={
                'unique_together': {('trans_id', 'trip_id')},
            },
        ),
        migrations.CreateModel(
            name='Place_Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_place', models.TextField(max_length=1000, null=True)),
                ('rate_place', models.FloatField()),
                ('place_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Place')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User')),
            ],
            options={
                'unique_together': {('user_id', 'place_id')},
            },
        ),
        migrations.CreateModel(
            name='Place_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.IntegerField()),
                ('image_of_place', models.ImageField(height_field=500, upload_to='', width_field=500)),
                ('place_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Place')),
            ],
            options={
                'unique_together': {('image_id', 'place_id')},
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_DnT', models.DateTimeField()),
                ('departure_DnT', models.DateTimeField()),
                ('place_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Place')),
                ('trip_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User_Input')),
            ],
            options={
                'unique_together': {('place_id', 'trip_id')},
            },
        ),
        migrations.CreateModel(
            name='Hotel_Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_booking_hotel', models.DateField()),
                ('charge_hotel', models.FloatField()),
                ('no_of_room', models.IntegerField()),
                ('hotel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.Hotel')),
                ('trip_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='travel.User_Input')),
            ],
            options={
                'unique_together': {('hotel_id', 'trip_id')},
            },
        ),
    ]