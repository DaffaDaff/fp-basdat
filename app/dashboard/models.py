from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User

# Create your models here.

class Biodata(models.Model):
    id_bio = models.AutoField(db_column='Id_Biodata', primary_key=True)
    username = models.ForeignKey(User, models.DO_NOTHING, db_column='username', to_field='username', blank=True, null=True)
    nama = models.CharField(db_column='Nama',  max_length=100, blank=True, null=True)
    nrp = models.CharField(db_column='NRP',  max_length=20, blank=True, null=True)  # Field name made lowercase.
    ttl = models.CharField(db_column='TTL', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'biodata'

    def __str__(self):
        return f'{self.nrp} - {self.nama}'


class Asisten(models.Model):
    id_asisten = models.AutoField(db_column='Id_Asisten', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='username', blank=True, null=True)
    id_praktikum = models.ForeignKey('Praktikum', models.DO_NOTHING, db_column='Id_Praktikum', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'asisten'

    nama_nrp = ''

    def __str__(self):
        nama = None
        nrp = None
        if self.user:
            nama = Biodata.objects.filter(username = self.user.username)
        if nama:
            nrp = nama.get().nrp
            nama = nama.get().nama
            
        
        return f'{nrp} - {nama} | {self.id_praktikum}'

class Jadwal(models.Model):
    id_jadwal = models.AutoField(db_column='Id_Jadwal', primary_key=True)
    id_kelompok = models.ForeignKey('Kelompok', models.DO_NOTHING, db_column='ID_Kelompok', blank=True, null=True)  # Field name made lowercase.
    id_modul = models.ForeignKey('Modul', models.DO_NOTHING, db_column='ID_Modul', blank=True, null=True)  # Field name made lowercase.
    id_asisten = models.ForeignKey(Asisten, models.DO_NOTHING, db_column='Id_Asisten', blank=True, null=True)  # Field name made lowercase.
    ruangan = models.CharField(db_column='Ruangan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jam = models.TimeField(db_column='Jam', blank=True, null=True)  # Field name made lowercase.
    tanggal = models.DateField(db_column='Tanggal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'jadwal'

    def __str__(self):
        return f'{self.id_modul} | {self.tanggal}-{self.jam} | Kelompok {self.id_kelompok.nama_kelompok}'

class Kelompok(models.Model):
    id_kelompok = models.AutoField(db_column='Id_Kelompok', primary_key=True)
    nama_kelompok = models.IntegerField(db_column='Nama_Kelompok', blank=True, null=True)
    id_praktikum = models.ForeignKey('Praktikum', models.DO_NOTHING, db_column='Id_Praktikum', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        db_table = 'kelompok'

    def __str__(self):
        return f'{self.id_praktikum} - Kelompok {self.nama_kelompok}'


class Modul(models.Model):
    id_modul = models.AutoField(db_column='Id_Modul', primary_key=True)
    id_praktikum = models.ForeignKey('Praktikum', models.DO_NOTHING, db_column='ID_Praktikum', blank=True, null=True)  # Field name made lowercase.
    modul_ke = models.IntegerField(db_column='Modul_Ke', blank=True, null=True)
    pdf_modul = models.FileField(db_column='File_Pdf', upload_to=f'modul', max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'modul'

    def __str__(self):
        return f'{self.id_praktikum} - Modul {self.modul_ke}'

class NilaiPraktikan(models.Model):
    id_nilai = models.AutoField(db_column='Id_Nilai', primary_key=True)
    id_jadwal = models.ForeignKey(Jadwal, models.DO_NOTHING, db_column='Id_Jadwal', blank=True, null=True)  # Field name made lowercase.
    id_praktikan = models.ForeignKey('Praktikan', models.DO_NOTHING, db_column='ID_Praktikan', blank=True, null=True)  # Field name made lowercase.
    nilai = models.IntegerField(db_column='Nilai', default=0, blank=True, null=True, validators=[MaxValueValidator(100), MinValueValidator(0)])  # Field name made lowercase.

    class Meta:
        db_table = 'nilai_praktikan'

    def __str__(self):
        nama = None
        nrp = None
        if self.id_praktikan.username:
            nama = Biodata.objects.filter(username = self.id_praktikan.username.username)
        if nama:
            nrp = nama.get().nrp
            nama = nama.get().nama
        return f'{nrp} - {nama} | {self.id_jadwal.id_modul}'

class Praktikan(models.Model):
    id_praktikan = models.AutoField(db_column='Id_Praktikan', primary_key=True)
    username = models.ForeignKey(User, models.DO_NOTHING, db_column='username', blank=True, null=True)  # Field name made lowercase.
    id_kelompok = models.ForeignKey('Kelompok', models.DO_NOTHING, db_column='Id_Kelompok', blank=True, null=True)  # Field name made lowercase.
    id_praktikum = models.ForeignKey('Praktikum', models.DO_NOTHING, db_column='Id_Praktikum', blank=True, null=True)  # Field name made lowercase.

    nama_nrp = ''

    class Meta:
        db_table = 'praktikan'

    def __str__(self):
        nama = None
        nrp = None
        if self.username:
            nama = Biodata.objects.filter(username = self.username.username)
        if nama:
            nrp = nama.get().nrp
            nama = nama.get().nama
            
        
        return f'{nrp} - {nama} | {self.id_praktikum}'
    
    
class Praktikum(models.Model):
    id_praktikum = models.AutoField(db_column='Id_Praktikum', primary_key=True)
    nama_praktikum = models.CharField(db_column='Nama_Praktikum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deskripsi = models.TextField(db_column='Deskripsi', blank=True, null=True)
    dosen = models.CharField(db_column='Dosen', max_length=255, blank=True, null=True)  # Field name made lowercase.
    praktikum_buka = models.BooleanField(db_column='Praktikum_Dibuka', default=False)

    class Meta:
        db_table = 'praktikum'

    def __str__(self):
        return self.nama_praktikum