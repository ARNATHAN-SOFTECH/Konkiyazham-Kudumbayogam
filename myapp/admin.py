
from django.contrib import admin
from .models import FamilyMember, Register, Announcement, FamilyUnit


# ============================================================
# ANNOUNCEMENT ADMIN
# ============================================================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'date',
        'issued_by',
        'send_notification',
    )

    search_fields = ('title', 'message', 'issued_by')

    list_filter = ('date', 'send_notification')


# ============================================================
# INLINE: CHILDREN UNDER FAMILY UNIT
# ============================================================

class ChildInline(admin.TabularInline):

    model = FamilyMember

    fk_name = 'family_unit'

    extra = 1

    fields = (
        'name',
        'gender',
        'mother',
        'father',
        'note',
    )


# ============================================================
# FAMILY UNIT ADMIN
# ============================================================

@admin.register(FamilyUnit)
class FamilyUnitAdmin(admin.ModelAdmin):

    list_display = (
        'husband',
        'wife',
    )

    search_fields = (
        'husband__name',
        'wife__name',
    )

    inlines = [ChildInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'husband':
            kwargs['queryset'] = FamilyMember.objects.filter(
                gender='Male'
            ).order_by('name')

        elif db_field.name == 'wife':
            kwargs['queryset'] = FamilyMember.objects.filter(
                gender='Female'
            ).order_by('name')

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )


# ============================================================
# FAMILY MEMBER ADMIN
# ============================================================

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'gender',
        'mother',
        'father',
        'family_unit',
        'note',
    )

    search_fields = (
        'name',
        'mother__name',
        'father__name',
    )

    list_filter = (
        'gender',
        'family_unit',
        'note',
    )

    fields = (
        'name',
        'gender',
        'mother',
        'father',
        'parent',
        'family_unit',
        'note',
        'user',
    )

    autocomplete_fields = (
        'mother',
        'father',
        'parent',
        'family_unit',
    )


# ============================================================
# REGISTER ADMIN
# ============================================================

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'first_name',
        'last_name',
        'gender',
        'mother',
        'father',
        'spouse',
        'profession',
        'country',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'profession',
    )

    list_filter = (
        'gender',
        'country',
        'profession',
        'married',
    )

    autocomplete_fields = (
        'mother',
        'father',
    )
