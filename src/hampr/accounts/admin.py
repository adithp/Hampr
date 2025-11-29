from django.contrib import admin


from .models import CustomUser,OTP,UserAddress,AuditLog,PasswordReset

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    pass



# @admin.register(UserDevice)
# class UserDeviceAdmin(admin.ModelAdmin):
#     pass




@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    pass


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    pass
