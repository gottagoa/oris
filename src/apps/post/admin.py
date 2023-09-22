from django.contrib import admin
from .models import Category, Service, Review, About, Contacts, Rewards, FAQ, Gallery, Rewards, Privacy
from .forms import ReviewAdminForm


admin.site.register(Service)
admin.site.register(About)
admin.site.register(Contacts)
admin.site.register(FAQ)
admin.site.register(Gallery)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Rewards)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm

admin.site.register(Privacy)