from django.contrib import admin

from . models import Service, Benefit, TeamMember, Contact, Banner

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin) :
    list_display = ('title', 'id', )
    readonly_fields = ('slug', )

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin) :
    list_display = ('title', 'id', )
    readonly_fields = ('slug', )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin) :
    list_display = ('fullname', 'id', )
    readonly_fields = ('slug', )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin) :
    list_display = ('fullname', 'mobile', 'id', )

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin) :
    list_display = ('title', 'id', )
    readonly_fields = ('slug', )