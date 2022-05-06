from django.http import JsonResponse
def uploadPhoto(request):
    print(1)
    if request.method == "POST" and request.FILES:
        file = request.FILES.get('file')
        print(file.name)
        return JsonResponse('sesai', safe=False)
