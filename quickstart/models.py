from django.db import models

class Fight(models.Model):
    fightid = models.AutoField(db_column='FightId', primary_key=True)  # Field name made lowercase.
    fighter_f = models.IntegerField(db_column='FighterF')  # Field name made lowercase.
    fighter_s = models.IntegerField(db_column='FighterS')  # Field name made lowercase.
    def __str__(self):
        return str(self.fightid)
    class Meta:
        db_table = 'fights'


