from django.db import models
from django.db.models import Model

class user(models.Model):
    user_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=100,null=False)
    mobile_no = models.CharField(max_length=20,null=False)
    password = models.CharField(max_length=100,null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=10,null=False,default='male')
    address = models.CharField(max_length=200,null=False)
    email_token = models.CharField(max_length=200,null=False,default='none')
    status = models.BooleanField()

    def __str__(self):
        return '%s' % (self.email)

class sports(models.Model):
    sports_id =   models.AutoField(primary_key=True)
    sports_name = models.CharField(max_length=100,null=False)

    def __str__(self):
        return '%s' % (self.sports_name)

class ground(models.Model):
    ground_id = models.AutoField(primary_key=True)
    sports = models.ForeignKey(sports, on_delete=models.CASCADE)
    ground_name = models.CharField(max_length=100,default='0000000')
    per_hour_charge = models.IntegerField(null=False,default=200)
    status = models.BooleanField()

    def __str__(self):
        return '%s' % (self.ground_name)

class team(models.Model):
    team_id = models.AutoField(primary_key=True)
    user  = models.ForeignKey(user,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100,null=False,default='0000000')
    sports = models.ForeignKey(sports,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return '%s' % (self.name)         
    
class booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user  = models.ForeignKey(user,on_delete=models.CASCADE)
    sports = models.ForeignKey(sports,on_delete=models.CASCADE)
    ground = models.ForeignKey(ground,on_delete=models.CASCADE)
    team = models.ForeignKey(team,on_delete=models.CASCADE,default=1)
    date = models.DateField()
    start_time = models.CharField(max_length=100,default='0000000')
    end_time = models.CharField(max_length=100,default='0000000')
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.ground.ground_name)
   

class player(models.Model):
    player_id = models.AutoField(primary_key=True)
    user  = models.ForeignKey(user,on_delete=models.CASCADE,default=1)
    team = models.ForeignKey(team,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100,null=False,default='0000000')
    gender = models.CharField(max_length=100,null=False)

    def __str__(self):
        return '%s' % (self.name)

class classes(models.Model):
    classes_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100,null=False)
    sports = models.ForeignKey(sports,on_delete=models.CASCADE,default=1)
    price = models.IntegerField(null=False)
    details = models.CharField(max_length=100,null=False,default='0000000')
    status = models.BooleanField() 

    def __str__(self):
        return '%s' % (self.name)   

class tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100,null=False)
    sports = models.ForeignKey(sports,on_delete=models.CASCADE,default=1)
    created_by = models.ForeignKey(user,on_delete=models.CASCADE,default=1,related_name='creator')
    team_1 = models.ForeignKey(team,on_delete=models.CASCADE,default=1,related_name='creator')
    accepted_user = models.ForeignKey(user,on_delete=models.CASCADE,default=1,related_name='accepter')
    team_2 = models.ForeignKey(team,on_delete=models.CASCADE,null=True,related_name='accepter')
    booking = models.ForeignKey(booking,null=True,on_delete=models.CASCADE)
    details = models.CharField(max_length=100,null=False,default='0000000')
    response = models.CharField(max_length=100,null=False,default='in waiting')
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.name)

class payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    total_amount = models.IntegerField(null=False)
    date = models.DateField(null=True)
    order_id = models.CharField(max_length=100,null=False)
    razorpay_order_id = models.CharField(max_length=100,null=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True)
    razorpay_signature_id = models.CharField(max_length=100,null=True)
    booking = models.ForeignKey(booking,null=True,on_delete=models.CASCADE)
    classes = models.ForeignKey(classes,null=True,on_delete=models.CASCADE)
    payment_type = (
        (1,'GROUND BOOKING'),
        (2,'FOR CLASS'),
    )
    payment_for = models.IntegerField(choices=payment_type,default=1)
    status_choise = (
        (1,'SUCCESS'),
        (2,'FAILURE'),
        (3,'PENDING'),
    )
    status = models.IntegerField(choices=status_choise,default=1)


    def __str__(self):
        return '%s' % (self.payment_id)
        
    



