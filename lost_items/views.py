from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import this to ensure the user is logged in
from django.contrib import messages  # Import the messages framework
from .forms import LostItemForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import csv
from difflib import SequenceMatcher
from .models import LostItem
from found_items.models import FoundItem
from django.db.models import Q  

@login_required  # This decorator ensures that only logged-in users can report a lost item
def is_similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.7

def report_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit yet
            lost_item = form.save(commit=False)
            lost_item.user = request.user  # Assign the logged-in user to the item

            # ------ Matching Logic Start -------
            item_name = lost_item.item_name
            lost_location = lost_item.lost_location

            # Check if any FOUND items match with the entered LOST item
            from found_items.models import FoundItem  # Import FoundItem model here (adjust if needed)

            matched_found_items = FoundItem.objects.filter(
                Q(item_name__icontains=item_name) & 
                Q(found_location__icontains=lost_location)
            )

            if matched_found_items.exists():
                # Instead of redirecting, render the match_found.html template with the matched items
                return render(request, 'home/match_found.html', {
                    'matched_found_items': matched_found_items,
                    'lost_item': lost_item
                })
            # ------ Matching Logic End -------

            lost_item.save()  # Now save the item with the user association

            # Add a success message
            messages.success(request, "Lost item has been successfully reported!")

            # Redirect to the home page
            return redirect('home')
    else:
        form = LostItemForm()

    return render(request, 'lost_items/report_lost_item.html', {'form': form})


def search_lost_items(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    lost_items = LostItem.objects.all()

    # Filter by search text
    if query:
        lost_items = lost_items.filter(item_name__icontains=query)

    # Filter by resolution status
    if status == 'resolved':
        lost_items = lost_items.filter(is_resolved=True)
    elif status == 'unresolved':
        lost_items = lost_items.filter(is_resolved=False)

    # Filter by category
    if category:
        lost_items = lost_items.filter(category__iexact=category)

    # Filter by date range
    if start_date:
        lost_items = lost_items.filter(lost_date__gte=start_date)
    if end_date:
        lost_items = lost_items.filter(lost_date__lte=end_date)

    lost_items = lost_items.order_by('-lost_date')

    return render(request, 'lost_items/search_lost_items.html', {
        'lost_items': lost_items,
        'query': query,
        'status': status,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
    })

def lost_item_detail(request, pk):
    # Retrieve a specific lost item by its primary key (pk)
    lost_item = get_object_or_404(LostItem, pk=pk)
    return render(request, 'lost_items/lost_item_detail.html', {'lost_item': lost_item})
from django.http import HttpResponseForbidden

def toggle_lost_item_status(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    # Check if the current user is the one who reported the item
    if item.user != request.user:
        messages.error(request, "❌ You are not authorized to change the status of this item.")
        return redirect('lost_items:search_lost_items')

    item.is_resolved = not item.is_resolved
    item.save()
    messages.success(request, "✅ Status updated successfully.")
    return redirect('lost_items:search_lost_items')

def export_lost_items_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lost_items_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Date Posted', 'Is Resolved'])

    for item in LostItem.objects.all():
        writer.writerow([item.title, item.description, item.date_posted, item.is_resolved])

    return response