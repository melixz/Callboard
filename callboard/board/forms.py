from django import forms
from .models import Announcement, Comment


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'text', 'category', 'image', 'video']
        exclude = ("likes",)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'category': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'style': 'width: 50%'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'style': 'width: 50%'}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields= ('content',)