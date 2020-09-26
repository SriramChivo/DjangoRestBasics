from django.contrib import admin
from .models import tweet
# Register your models here.


class tweetAdmin(admin.ModelAdmin):
    model = tweet
    # we can use form also as a admin interface
    readonly_fields = ["date_created", "updatedTime"]
    fields = ["User", "Title", "content",
              "image", "date_created", "updatedTime"]
    list_display = ["Title", "__str__", "image", "date_created"]
    search_fields = ["content"]


# if you addonly modeladmin then it throws an error that for model in model_or_iterable:
# TypeError: 'MediaDefiningClass' object is not iterable
admin.site.register(tweet, tweetAdmin)
