from django.contrib.auth.base_user import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, email, cname, password=None, **fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(email=email, cname=cname, **fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, cname, password, **fields):
        user = self.create_user(email, cname, password=password, **fields)
        user.is_superuser = True
        user.save()
        return user
