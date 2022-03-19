from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def has_neighbourhood(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.neighbourhood is not None:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Please update your neighbourhood.')
            return redirect('profile')

    return wrap
