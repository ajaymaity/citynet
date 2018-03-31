"""Dashboard views."""
import os

from django.shortcuts import render


def rtDemo(request):
    """Serve the index."""
    return render(request, "rtDemo.html", {'hostname':
                                           os.environ.get("HOSTNAME", "None")})
