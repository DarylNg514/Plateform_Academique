from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        return {
            'unread_messages_count': Message.objects.filter(destinataire=request.user, lu=False).count()
        }
    return {}
