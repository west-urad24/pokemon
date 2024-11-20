from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    no = models.IntegerField()
    abilities = models.JSONField()  # 特性のリストをJSONフィールドに保存
    types = models.JSONField()  # タイプのリスト
    height = models.FloatField()
    weight = models.FloatField()
    evolutions = models.JSONField(null=True, blank=True)  # 進化情報
    level_up_moves = models.JSONField(null=True, blank=True)  # レベルアップで覚える技
    tms = models.JSONField(null=True, blank=True)  # わざマシン
    trs = models.JSONField(null=True, blank=True)  # わざレコード
    egg_moves = models.JSONField(null=True, blank=True)  # たまごわざ


    def __str__(self):
        return self.name

class Item(models.Model):
    ja_item = models.CharField(max_length=255)
    en_item = models.CharField(max_length=255)


    def __str__(self):
        return self.ja_item
