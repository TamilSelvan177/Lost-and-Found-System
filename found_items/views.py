from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FoundItemForm
from difflib import SequenceMatcher
from lost_items.models import LostItem
from .models import FoundItem
from django.db.models import Q
from django.utils.dateparse import parse_date

@login_required
def is_similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.7

def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user  # Assign the logged-in user to the found item

            # ------ Matching Logic Start -------
            item_name = found_item.item_name
            found_location = found_item.found_location

            # Check if any LOST items match with the entered FOUND item
            from lost_items.models import LostItem  # Import LostItem model here (adjust if needed)

            matched_lost_items = LostItem.objects.filter(
                Q(item_name__icontains=item_name) & 
                Q(lost_location__icontains=found_location)
            )

            if matched_lost_items.exists():
                # If a match is found, render the match_found.html template
                return render(request, 'home/match_lost.html', {
                    'matched_lost_items': matched_lost_items,
                    'found_item': found_item,
                    'type': 'Found'
                })
            # ------ Matching Logic End -------

            found_item.save()  # Save the found item

            # Add a success message
            messages.success(request, "Found item has been successfully reported!")

            # Redirect to the home page
            return redirect('home')
    else:
        form = FoundItemForm()

    return render(request, 'found_items/report_found_item.html', {'form': form})



def search_found_items(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    found_items = FoundItem.objects.all()

    if query:
        found_items = found_items.filter(item_name__icontains=query)

    if status == 'resolved':
        found_items = found_items.filter(is_resolved=True)
    elif status == 'unresolved':
        found_items = found_items.filter(is_resolved=False)

    if category:
        found_items = found_items.filter(category__icontains=category)

    if start_date:
        found_items = found_items.filter(found_date__gte=parse_date(start_date))

    if end_date:
        found_items = found_items.filter(found_date__lte=parse_date(end_date))

    found_items = found_items.order_by('-found_date')

    return render(request, 'found_items/search_found_items.html', {
        'found_items': found_items,
        'query': query,
        'status': status,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
    })


def found_item_detail(request, pk):
    found_item = get_object_or_404(FoundItem, pk=pk)
    return render(request, 'found_items/found_item_detail.html', {'found_item': found_item})

from django.http import HttpResponseForbidden



def toggle_found_item_status(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)

    # Check if the current user is the one who reported the item
    if item.user != request.user:
        messages.error(request, "❌ You are not authorized to change the status of this item.")
        return redirect('found_items:search_found_items')

    item.is_resolved = not item.is_resolved
    item.save()
    messages.success(request, "✅ Status updated successfully.")
    return redirect('found_items:search_found_items')