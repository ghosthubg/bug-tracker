from django.contrib import admin
from .models import Bug, BugComment, Developer,AssignedDeveloper,ChangeStatus
# Register your models here.



admin.site.register(Bug)
admin.site.register(BugComment)
admin.site.register(Developer)
admin.site.register(AssignedDeveloper)
admin.site.register(ChangeStatus)



