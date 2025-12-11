from django import forms
from .models import Comment, NewsletterSubscriber
from mptt.forms import TreeNodeChoiceField

class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ('content', 'parent')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-4 border rounded-lg focus:ring-2 focus:ring-indigo-500', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()


class NewsSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email',)