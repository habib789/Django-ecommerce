from django import forms
from .models import Post, PostComment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'post_image', 'user')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'type': 'hidden', 'value': '', 'id': 'usr'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('text', 'user')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'user': forms.TextInput(attrs={'type': 'hidden', 'value': '', 'id': 'usr'}),
        }
