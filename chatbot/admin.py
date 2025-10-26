from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    can_delete = False
    readonly_fields = ("sender", "message", "timestamp")
    fields = ("timestamp", "sender", "message")
    ordering = ("-timestamp",)
    

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("user_name", "business_type", "context", "started_at")
    list_filter = ("context", "started_at")
    search_fields = ("user_name", "business_type")
    date_hierarchy = "started_at"
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "sender", "short_message", "timestamp")
    list_filter = ("sender", "timestamp", "session__context")
    search_fields = ("message", "session__user_name", "session__business_type")
    date_hierarchy = "timestamp"

    def short_message(self, obj):
        return (obj.message[:80] + "…") if len(obj.message) > 80 else obj.message
    short_message.short_description = "Mensagem"
