from django import forms
from .models import Category, Review




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent']



class ReviewAdminForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1, widget=forms.NumberInput())

    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Оцените прием у специалиста от 1 до 5')
        return rating

 