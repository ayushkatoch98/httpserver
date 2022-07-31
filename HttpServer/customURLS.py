from views import index , notFound

# /path/ and /path are considered two different paths
urls = {
    "/" : index,
    "/index" : index,
    "/404" : notFound,
}

# users shouldnt call this function manually
def execute(request):
    status = 200
    
    if request["path"] not in urls:
        func = urls["/404"]
    else:
        func = urls[request["path"]]

    status , file = func(request)
    return status , open(file).read()