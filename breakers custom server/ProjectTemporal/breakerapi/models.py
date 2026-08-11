from django.db import models



class PatrollerUser(models.Model):
    userID = models.PositiveBigIntegerField(primary_key=True) #289193220923131928 is mine #TODO: double check if an autofield would work here
    gameCurrency = models.JSONField()
    messageList = models.JSONField()
    rivalList = models.JSONField()
    userCharacters = models.JSONField()
    #skills
    
    
    
class MessageBot(models.Model):
    messageID = models.CharField(max_length=32, primary_key=True) #example: 20260313_CosMatch
    messageContents = models.JSONField()

    