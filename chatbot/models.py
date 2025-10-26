from django.db import models


class ChatSession(models.Model):
    user_name = models.CharField(max_length=150, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    context = models.CharField(max_length=50, default='geral')
    started_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user_name or "Visitante"} - ({self.context})'


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[{'user', 'Usuário'}, {'bot', 'Bot'}])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.sender}: {self.message[:40]}...'
    