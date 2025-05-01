from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'home/edit_profile.html', {'form': form})
def profile(request):
    return render(request, 'home/profile.html', {'user': request.user})
def landing_page(request):
    return render(request, 'home/landing.html')
def home_view(request):
    return render(request, 'home/home.html') 
def about(request):
    return render(request, 'home/about.html')
def contact(request):
    return render(request, 'home/contact.html')
