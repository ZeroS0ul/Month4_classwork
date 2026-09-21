from django import forms
from posts.models import Comment
from posts.models import Post

BANNED_WORDS = ("war", "ban", "BEGIN")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "image", "category", "tags")

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title in BANNED_WORDS:
            raise forms.ValidationError("title has banned word!")

        return title





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "text",
            "category",
            "tags",
            "image",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "text"]

        widgets = {
            "author_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваше имя",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Напишите комментарий...",
                    "rows": 4,
                }
            ),
        }
