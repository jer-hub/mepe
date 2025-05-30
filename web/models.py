# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WebFarsl(models.Model):
    fid = models.SmallIntegerField(db_column='fID', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='fName', max_length=99, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'web_farsl'


class WebMcust(models.Model):
    fid = models.PositiveIntegerField(db_column='fID', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='fName', max_length=90, blank=True, null=True)  # Field name made lowercase.
    fpassword = models.CharField(db_column='fPassword', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'web_mcust'


class WebPcust(models.Model):
    fauto = models.AutoField(db_column='fAUTO', primary_key=True)
      # Field name made lowercase.
    fcust = models.ForeignKey(WebMcust, db_column='fCUST', on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    # fcust = models.PositiveIntegerField(db_column='fCUST')  # Field name made lowercase.
    fsl = models.ForeignKey(WebFarsl, db_column='fSL', on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    # fsl = models.SmallIntegerField(db_column='fSL', blank=True, null=True)  # Field name made lowercase.
    fdoc = models.CharField(db_column='fDoc', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fsdate = models.CharField(db_column='fsDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    frem = models.CharField(db_column='fRem', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fsdr = models.CharField(db_column='fsDr', max_length=18, blank=True, null=True)  # Field name made lowercase.
    fscr = models.CharField(db_column='fsCr', max_length=18, blank=True, null=True)  # Field name made lowercase.
    fsbal = models.CharField(db_column='fsBal', max_length=18, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'web_pcust'
