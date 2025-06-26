from django.shortcuts import render, redirect
from .models import WebPcust

# Create your views here.
def checkaccount(request):
    if request.method == 'POST':
        try:
            chapa = request.POST.get("chapa", "").strip()
            if not chapa:
                return render(request, 'web/checkaccount.html', {'error': 'Please enter a valid member ID'})
            
            instances = WebPcust.objects.filter(fcust__fid=chapa)
            if instances.exists():
                return redirect("web:particulars", chapa=chapa)
            else:
                return render(request, 'web/checkaccount.html', {'error': 'Invalid credentials'})
        except (ValueError, KeyError) as e:
            return render(request, 'web/checkaccount.html', {'error': 'Invalid member ID format'})
        except Exception as e:
            return render(request, 'web/checkaccount.html', {'error': 'An error occurred. Please try again.'})
    return render(request, 'web/checkaccount.html')

def particulars(request, chapa):
    try:
        # Validate chapa parameter
        if not chapa or not str(chapa).strip():
            return render(request, 'web/checkaccount.html', {'error': 'Invalid member ID'})
        
        instances = WebPcust.objects.filter(fcust__fid=chapa)
        
        # Safely get member name
        name = None
        if instances.exists():
            try:
                name = instances.first().fcust.fname
            except (AttributeError, ValueError):
                name = "Unknown Member"
        
        # Safely get particulars list
        try:
            particulars = instances.values_list("fsl__fname", flat=True).distinct()
        except (ValueError, AttributeError):
            particulars = []
          # Store the base queryset for filtering
        base_instances = instances
        
        # Handle filter functionality with error checking
        selected_particular = request.GET.get('particular', '').strip()
        if selected_particular:
            try:
                instances = instances.filter(fsl__fname=selected_particular)
            except (ValueError, TypeError):
                # Reset to original instances if filter fails
                instances = base_instances
                selected_particular = None
        
        # Handle search functionality with error checking
        search_query = request.GET.get('search', '').strip()
        if search_query:
            try:
                # Limit search query length to prevent issues
                if len(search_query) > 100:
                    search_query = search_query[:100]
                # Apply search filter on top of existing filters (particular + search combined)
                instances = instances.filter(fdoc__icontains=search_query)
            except (ValueError, TypeError):
                # Reset to base instances and reapply particular filter if it exists
                instances = base_instances
                if selected_particular:
                    try:
                        instances = instances.filter(fsl__fname=selected_particular)
                    except (ValueError, TypeError):
                        instances = base_instances
                        selected_particular = None
                search_query = None
        
        if instances.exists() or selected_particular or search_query:  # Show page even when filtered/searched result is empty
            return render(request, 'web/particulars.html', {
                'instances': instances, 
                'name': name, 
                'particulars': particulars, 
                'chapaID': chapa,
                'selected_particular': selected_particular,
                'search_query': search_query
            })
        else:
            return render(request, 'web/checkaccount.html', {'error': 'Invalid credentials'})
    
    except (ValueError, TypeError) as e:
        # Handle value/type errors
        return render(request, 'web/checkaccount.html', {'error': 'Invalid member ID format'})
    
    except Exception as e:
        # Handle any other unexpected errors
        return render(request, 'web/checkaccount.html', {'error': 'An error occurred. Please try again.'})
