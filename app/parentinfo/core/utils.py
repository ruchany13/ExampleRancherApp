from .models import Institution

def institution_for(user):
    if user.is_superuser:
        return None  # superuser için sınırsız; admin tarafında özel ele alacağız
    # Kullanıcının yönettiği kurumu döndür (yoksa None)
    return getattr(user, "managed_institution", None)