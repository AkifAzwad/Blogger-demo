from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField
# Create your models here.

User = get_user_model()


class PostView(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name = _("PostView")
    #     verbose_name_plural = _("PostViews")

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("PostView_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        "Post", related_name='comments', on_delete=models.CASCADE)

    # class Meta:
    # verbose_name = _("Comment")
    # verbose_name_plural = _("Comments")

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("Comment_detail", kwargs={"pk": self.pk})


class Author(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    # class Meta:
    #     verbose_name = _("Author")
    #     verbose_name_plural = _("Authors")

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("Author_detail", kwargs={"pk": self.pk})


class Category(models.Model):

    title = models.CharField(max_length=50)

    # class Meta:
    #     verbose_name = _("Category")
    #     verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("Category_detail", kwargs={"pk": self.pk})


class Post(models.Model):

    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField('Content')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # comment_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    thumbnail = models.ImageField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        "self", related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        "self", related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    # class Meta:
    #     verbose_name = _("Post")
    #     verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("post-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": self.id})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
