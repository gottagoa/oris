from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Service, Review, About, Contacts, Rewards, AboutType, FAQ, Gallery, Privacy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReviewAdminForm
from src.apps.account.models import User, Doctor
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

"""
Category
"""

def index(request):
    categories=Category.objects.all()
    doctors=Doctor.objects.all()
    reviews=Review.objects.all()
    service=Service.objects.all()
    about_category=About.objects.get(page=AboutType.CATEGORIES)
    about_index=About.objects.filter(page=AboutType.INDEX)
    about_services=About.objects.get(page=AboutType.SERVICES)
    about_categories=About.objects.get(page=AboutType.CATEGORIES)
    about_faq=About.objects.get(page=AboutType.FAQ)
    faqs=FAQ.objects.all()
    gallery=Gallery.objects.all()
    

    context = {
        'categories':categories,
        'doctors':doctors,
        'reviews':reviews,
        'services':service,
        'categories':categories,
        'about_category': about_category,
        'about_us': About.objects.get(page=AboutType.ABOUT),
        "quantity": Doctor.objects.count(),
        "quantity_categories":Category.objects.count(),
        'rewards': Rewards.objects.all(),
        'quantity_rewards':Rewards.objects.count(),
        'about_index': about_index,
        'about_services':about_services,
        'about_categories':about_categories,
        'about_faq':about_faq,
        'faqs':faqs,
        'gallery':gallery
        
    }
    return render(request, 'index.html', context)


    
def about_us(request):
    about=About.objects.get(page=AboutType.ABOUT)

    context = {
        "about": about,
        "quantity": Doctor.objects.count(),
        "quantity_categories":Category.objects.count(),
        'rewards': Rewards.objects.all(),
        "quantity_rewards": Rewards.objects.count(),
       
    }
        
    return render(request, 'about_us.html', context)


def services(request):
    about = About.objects.get(page=AboutType.SERVICES)
    services=Service.objects.all()
    context = {
        "about": about,
        'services': services
    }
    return render(request, 'services.html', context)


def get_categories(request):
    about=About.objects.get(page=AboutType.CATEGORIES)
    categories = Category.objects.all()
    context = {
        "about": about,
        "categories": categories
    }
    return render(request, "category_list.html", context)


def get_categories_index(request):
    about=About.objects.filter(page=AboutType.CATEGORIES).first()
    categories = Category.objects.all()
    context = {
        "about": about,
        "categories": categories
    }
    return render(request, "index.html", context)


def category_template(request, id):
    category = get_object_or_404(Category, pk=id)
    context = {
        'category': category,
    }
    return render(request, 'category_template.html', context)



"""
Review
"""

@login_required(login_url='login')
def create_review(request, doctor_id):
    patient = request.user.patient
    user = User.objects.get(pk=doctor_id)
    doctor = user.doctor

    if request.method == 'POST':
        print(request.POST)
        form = ReviewAdminForm(request.POST)
        
        if form.is_valid():
            if hasattr(request.user, 'doctor') and request.user.doctor == doctor:
                return HttpResponse("Вы не можете оставить отзыв себе")
            review = form.save(commit=False)
            review.patient = patient
            review.doctor = doctor
            review.save()
            return redirect(reverse("doctor_template", kwargs={"pk": doctor_id}))



@login_required(login_url='login')
def create_common_review(request):
    patient = request.user.patient
    reviews = Review.objects.all() 


    if request.method == 'POST':
        form = ReviewAdminForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.patient = patient
            review.save()
            return redirect('review_list')
    else:
        form = ReviewAdminForm()
    
    return render(request, 'create_common_review.html', {'form': form, 'reviews': reviews})




@login_required(login_url='login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user.patient != review.patient:
        return redirect('review_list') 
    
    if request.method == 'POST':
        form = ReviewAdminForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewAdminForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})


@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user.patient != review.patient:
        return redirect('review_list') 
    
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'review_list.html', {'review': review})



def review_list(request):
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 12) 
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    return render(request, 'review_list.html', {'reviews': page_reviews})


def doctor_reviews(request, doctor_id):
    requested_doctor = get_object_or_404(Doctor, pk=doctor_id)
    reviews = Review.objects.filter(doctor=requested_doctor)
    paginator = Paginator(reviews, 3)  
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    return render(request, 'doctor_reviews.html', {'requested_doctor': requested_doctor, 'reviews': page_reviews})




def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq_list.html', {'faqs': faqs})

def reward_list(request):
    rewards = Rewards.objects.all()
    return render(request, 'rewards_list.html', {'rewards': rewards})

"""
Service
"""

def split_description(description):
    sentences = description.split('. ')
    return sentences

def get_service(request, id):
    service = get_object_or_404(Service, pk=id)
    description = service.description
    description_sentences = split_description(description)
    context = {
        'service': service,
        'description_sentences': description_sentences,
    }
    return render(request, 'service_template.html', context)


def view_privacy(request):
    description=Privacy.objects.all()
    return render(request, 'privacy.html', {'description': description})


