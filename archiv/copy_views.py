from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Site, ArchEnt, ResearchEvent, MonumentProtection


@login_required
def copy_site_poly_view(request):

    """copies the current's object polygon to a new target_class"""

    CLASSES = {
        'Site': Site,
        'ResearchEvent': ResearchEvent,
        'ArchEnt': ArchEnt,
        'MonumentProtection': MonumentProtection,
    }

    current_id = request.GET.get('current-id', '')
    current_class = request.GET.get('current-class', '')
    target_class = request.GET.get('target-class', '')
    if current_id and current_class and target_class:
        source_object = CLASSES[current_class].objects.get(id=current_id)
        target_object = CLASSES[target_class].objects.create()
        target_object.polygon = source_object.polygon
        target_object.name = "POLYGON COPIED FROM {}".format(source_object)
        target_object.save()
        return redirect(target_object)
    else:
        html = "<html><body>Something went wrong</body></html>"
        return HttpResponse(html)
