from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import git


@csrf_exempt
def update(request):
    if request.method != "POST":
        return HttpResponse("Method not  allowed", status=405)
    
    if request.headers.get("x-github-Event") != "push":
        return HttpResponse("Ignored", status=200)

    try:
        repo = git.Repo("/home/LuanLopS/Django_restfull")
        origin = repo.remotes.origin

        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def hello_world(request):
    template = loader.get_template("hello_world.html")
    return HttpResponse(template.render())
