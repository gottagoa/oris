from .models import Category, Contacts


def get_categories(request):
    return {"categories": Category.objects.filter(parent__isnull=True)}

def contacts_view(request):
    contacts = Contacts.objects.all().first() 
    context = {
        'contacts': contacts
    }
    
    return context 