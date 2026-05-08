from django.contrib import admin
from .models import FamilyMember, Register, Announcement, FamilyUnit

admin.site.register(Announcement)

# -----------------------------
# INLINE: CHILDREN UNDER MARRIAGE
# -----------------------------
class ChildInline(admin.TabularInline):
    model = FamilyMember
    fk_name = "family_unit"
    extra = 1


# -----------------------------
# FAMILY UNIT ADMIN
# -----------------------------
@admin.register(FamilyUnit)
class FamilyUnitAdmin(admin.ModelAdmin):
    list_display = ("husband", "wife")
    search_fields = ("husband__name", "wife__name")

    inlines = [ChildInline]


# -----------------------------
# FAMILY MEMBER ADMIN
# -----------------------------
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "family_unit", "note")  
    search_fields = ("name",)
    list_filter = ("parent", "family_unit","note")

    fields = ("name", "parent", "family_unit", "note", "user")


# -----------------------------
# REGISTER ADMIN
# -----------------------------
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "parent", "profession", "country")
    search_fields = ("first_name", "last_name", "email", "profession")
    list_filter = ("country", "profession")