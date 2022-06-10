from django.contrib import admin
from .models import user,sports,ground,booking,player,team,classes,tournament,payment



class useradminModel(admin.ModelAdmin):
    search_fields=('user_id','first_name','last_name','gender','email','mobile_no','age','address')
    list_display=('user_id','first_name','last_name','gender','email','mobile_no','age','address')

admin.site.register(user, useradminModel)

class sportsadminModel(admin.ModelAdmin):
    search_fields=('sports_name','sports_id')
    list_display=('sports_name','sports_id')

admin.site.register(sports,sportsadminModel)

class groundadminModel(admin.ModelAdmin):
    search_fields=('ground_id','sports','ground_name','per_hour_charge','status')
    list_display=('ground_id','sports','ground_name','per_hour_charge','status')

admin.site.register(ground,groundadminModel)

class bookingadminModel(admin.ModelAdmin):
    search_fields=('booking_id','user','sports','ground','team','date','start_time','end_time','status')
    list_display=('booking_id','user','sports','ground','team','date','start_time','end_time','status')

admin.site.register(booking,bookingadminModel)

class playeradminModel(admin.ModelAdmin):
    search_fields=('player_id','user','team','name','gender')
    list_display=('player_id','user','team','name','gender')

admin.site.register(player,playeradminModel)    

class teamadminModel(admin.ModelAdmin):
    search_fields=('team_id','user','name','sports')
    list_display=('team_id','user','name','sports')

admin.site.register(team,teamadminModel)

class classesadminModel(admin.ModelAdmin):
    search_fields=('classes_id','name','sports','price','details')
    list_display=('classes_id','name','sports','price','details')

admin.site.register(classes,classesadminModel)

class tournamentadminModel(admin.ModelAdmin):
    search_fields=('tournament_id','name','sports','created_by','team_1','accepted_user','team_2','booking','response','details')
    list_display=('tournament_id','name','sports','created_by','team_1','accepted_user','team_2','booking','response','details')

admin.site.register(tournament,tournamentadminModel)

class paymentadminModel(admin.ModelAdmin):
    search_fields=('payment_id','user','total_amount','date','order_id','razorpay_order_id','razorpay_payment_id','razorpay_signature_id','status')
    list_display=('payment_id','user','total_amount','date','order_id','razorpay_order_id','razorpay_payment_id','razorpay_signature_id','status')

admin.site.register(payment,paymentadminModel)






