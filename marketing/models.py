from django.db import models

# Create your models here.
class Signup(models.Model):

    email = models.EmailField(max_length=254)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    

    # class Meta:
    #     verbose_name = _("Signup")
    #     verbose_name_plural = _("Signups")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("Signup_detail", kwargs={"pk": self.pk})
