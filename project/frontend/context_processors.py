import settings

def globals(request):
    return {
            'MEDIA_URL' : settings.MEDIA_URL
    }
    
