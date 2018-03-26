from django import forms
from tvtrail.models import UserProfile, episode_comment
from tvtrail.models import user_show_relation
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = UserProfile
        #fields = ('watchlist',)
        exclude = ('user', 'watchlist')

class EpisodeCommentForm(forms.ModelForm):

    class Meta:
        model = episode_comment
        fields = ('text',)
        exclude = ('author', 'episode_id')
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'comment-text', 
                'required': True, 
                'placeholder': 'Say something...'
            }),
        }