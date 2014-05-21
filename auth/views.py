from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from auth.forms import PROFILE_FORM
from auth.models import PROFILE_CLASS
from auth.utils import get_profile

@login_required(login_url='/accounts/login/')
def edit_user_profile(request):

    try:
        instance = get_profile(request.user) 
    except:
        instance = PROFILE_CLASS(user=request.user)
    
    form = PROFILE_FORM(instance=instance)

    if request.method == 'POST':        
        form = PROFILE_FORM(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        
    return render(request, 'user_profile.html', {"form": form})


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))

def validation_sent(request):
    return render_to_response('validation_sent.html', {
        'email': request.session.get('email_validation_address')
    }, RequestContext(request))


def home(request):
    return render_to_response('home.html', {'profile':request.user_profile}, RequestContext(request))
    
