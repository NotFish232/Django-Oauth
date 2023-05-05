from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from requests_oauthlib import OAuth2Session
from new_blog.settings import CLIENT_ID, CLIENT_SECRET
import requests


oauth = OAuth2Session(CLIENT_ID)
auth_url = "https://ion.tjhsst.edu/oauth/authorize"
token_url = "https://ion.tjhsst.edu/oauth/token"


def home_page(request):
    ctx = {
        "authorized": oauth.authorized
    }
    return render(request, "home.html", ctx)

def login_page(request):
    url, state = oauth.authorization_url(auth_url)
    request.session["state"] = state
    return redirect(url)

def complete_page(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if state != request.session["state"]:
        return HttpResponse("You don't have the right state")
    del request.session["state"]

    token =  oauth.fetch_token(token_url, code, client_secret=CLIENT_SECRET)

    return redirect(home_page)
