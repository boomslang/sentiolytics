from django.db import models

class Match_info(models.Model): # TODO:(murat) Bunu test icin yazmistin, degistir.
    match_id = models.PositiveIntegerField()

#class player(models.Model):
#    id = models.
#
#
#    created = models.DateTimeField(auto_now_add=True)
#    author = models.CharField(max_length=60)
#    body = models.TextField()
#    post = models.ForeignKey(Post)