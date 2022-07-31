def index(request):
    if request["type"] == "GET":
        return 200, "templates/index.html"

def notFound(request):
    return 404, "templates/404.html"