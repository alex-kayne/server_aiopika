from django.db import models


class CatalogsData(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(null=True)
    catalog_name = models.TextField(null=True, db_index=True)

    class Meta:
        db_table = 'catalogs_data'
