from django import forms
from tinymce import TinyMCE
from .models import Post, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title','overview','thumbnail','categories','featured','content',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
                                                           'placeholder': 'type your comment here',
                                                           'id': 'usercomment',
                                                           'rows': 4}))

    class Meta:
        model = Comment
        fields = ('content',)
