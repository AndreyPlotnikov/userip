from django.http import JsonResponse
from . import models

# Create your views here.


def link(request):
    user1 = request.GET.get('user1')
    user2 = request.GET.get('user2')
    if not (user1 and user2):
        return JsonResponse({'error': 'Missing request params (user1, user2)'}, status=400)
    try:
        user1 = int(user1)
        user2 = int(user2)
    except ValueError:
        return JsonResponse({'error': 'Invalid request params'}, status=400)
    linked = models.check_link(user1, user2)
    data = {'linked': linked}
    return JsonResponse(data)