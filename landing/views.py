from django.shortcuts import render
import datetime
from .forms import SubscriberForm

def landing(request):
    current_date = datetime.date.today()
    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
        data = form.cleaned_data
        print(data['name'])

        form.save()

    return render(request, 'landing/landing.html', locals())
