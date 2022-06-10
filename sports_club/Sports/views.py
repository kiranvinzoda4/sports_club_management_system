from django.shortcuts import render, HttpResponse, redirect
from Sports.models import user,sports,ground,booking,player,team,classes,tournament,payment
from django.db.models import Q
import json
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from operator import itemgetter
from itertools import *
from .helpers import send_email_pass_forgot,send_email_to_active_user
import razorpay
from uuid import uuid4
import re



def home(request):
    return render(request,"home.html")

def profile2(request):
    if request.session['user_id']== "":
        return render(request,"home.html")

    user_id = request.session['user_id']
    print(user_id)
    data = user.objects.get(user_id=user_id)
    display = "none"
    display2 = "block"
    tournament_data = tournament.objects.filter(Q(accepted_user = data) & (Q(response="accepted") | Q(response="in waiting")))
    return render(request,"profile2.html",{'display':display,'display2':display2,'data' : data,"tournament":tournament_data})

def logout(request):
    request.session['user_id'] = ""
    return render(request,"home.html")    

def login(request):
    if request.method == 'POST':
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        username = request.POST["email"]
        password = request.POST["password"]
        data ={}
        if re.search(regex,username):
            print("Valid email")
        else:
            data['email'] = "Invalid email"

        if username == "" :
            data['email'] = "please enter email"

        if password == "" :
            data['pass'] = "please enter password"

        print(data)
        if bool(data): 
            return render(request,"login_page.html",{"data" : data })    
     
        test = user.objects.get(Q(email=username) & Q(password=password))
        
        user_id = test.user_id
         
        if test:
            print(test.status)
            if not test.status:
                data['error']= "your account is not active"
                return render(request,"login_page.html",{"data" : data })
            print(user_id)
            request.session['user_id'] = user_id
            data = user.objects.get(user_id = user_id)
            tournament_data = tournament.objects.filter(Q(accepted_user=data) & (Q(response="accepted") | Q(response="in waiting")))
            display = "none"
            display2 = "block"
            return render(request,"profile2.html",{"display2":display2,"data" : data,"tournament":tournament_data,"display":display })
        else:
            data['error'] = "username or password is wrong"
            return render(request,"login_page.html",{"data" : data })
    if request.method == 'GET':
       return render(request,"login_page.html")


def login_page(request):
    return render(request,"login_page.html")

def registration_page(request):
    return render(request,"registration_page.html")    

def about_us(request):
    return render(request,"about_us.html")  

def contact_us(request):
    return render(request,"contact_us.html")      

def register_user(request):
    if request.method == "POST":
        message = {}
        fname = request.POST["fname"]

        if fname == "":
            message['fname'] = "enter your name"
        if fname.isnumeric():
            message['fname'] = "do not use number as your name"   

        lname = request.POST["lname"]

        if lname == "":
            message['lname'] = "enter your name"
        if lname.isnumeric():
            message['lname'] = "do not use number as your name" 

        user_email = request.POST["user_email"]

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if user_email == "":
            message['user_email'] = "enter your email"
        if not re.search(regex,user_email):
            message['user_email'] = "invalide email"
        
        user_password = request.POST["user_pass"]
        if user_password == "":
            message['user_pass'] = "enter your password"

        mobile = request.POST["mobile_no"] 
        if mobile == "":
            message['mobile'] = "enter your mobile no."
        if len(mobile) != 10:
            print(len(mobile))
            message['mobile'] = "enter valid mobile number"     
        if not mobile.isnumeric():
            message['mobile'] = "use number as your mobile no."
        if mobile.isnumeric():
            mobile = int(mobile)    
                
        age = request.POST["age"] 
        if age == "":
            message['age'] = "enter your age"
        if len(age) > 2:
            message['age'] = "enter valid age"    
        if not age.isnumeric():
            message['age'] = "use number as your age"
        if age.isnumeric():
            age = int(age)
        
        user_address = request.POST["address"]
        if user_address == "":
            message['user_address'] = "enter your address"

        details = {"fname":fname,"lname":lname,"user_email":user_email,"user_password":user_password,"mobile":mobile,"age":age,"user_address":user_address}
        print(message)
        if bool(message):
            return render(request,"registration_page.html",{"data" : message,"details":details})             

        if not message:
            user_check = user.objects.filter(email=user_email).exists()
            if user_check:
                message['exist'] = "email is already registerd"
                return render(request,"registration_page.html",{"data" : message,"details":details}) 
            insert = user.objects.create(first_name=fname,last_name=lname,email=user_email,mobile_no=mobile,password=user_password,age=age,address=user_address,status=False)
            data = user.objects.get(email = user_email)
            token = str(uuid4())   
            send_email_to_active_user(data, token)  
            data.email_token = token
            data.save()
            return render(request,"message.html",{"message":"to activate your profile click the link we have sent to your email"})
        print(data)
        if data:
            display = "none"
            display2 = "block"
            request.session['user_id'] = data.user_id
            return render(request,"profile2.html",{"display2":display2,"data" : data,"display":display })
    if request.method == "GET":
        if request.session['user_id'] == "":
            return render(request,"home.html")
        data = user.objects.get(user_id = request.session['user_id'])
        display = "none"
        display2 = "block"
        return render(request,"profile2.html",{"display2":display2,"data" : data,"display":display })

def active_user(request,token):
    user_data = user.objects.get(email_token = token)
    if user_data:
        user_data.status = True
        user_data.email_token = "none"
        user_data.save()
        return render(request,"message.html",{"message":"profile is activate now you can login"})


def edit_profile(request):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    user_id = request.session['user_id']
    data = user.objects.get(user_id=user_id)
    return render(request, "edit_profile.html",{'data' : data})

def uptade_profile(request):
    if request.method == 'POST':
        
        message = {}
        fname = request.POST["fname"]

        if fname.isnumeric():
            message['fname'] = "do not use number as your name" 
        if fname == "":
            message['fname'] = "dont leave field empty"
          
        lname = request.POST["lname"]
        if lname.isnumeric():
            message['lname'] = "do not use number as your name"
        if lname == "":
            message['lname'] = "dont leave field empty"
         
        user_email = request.POST["email"]
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex,user_email):
            message['user_email'] = "invalide email"
        if user_email == "":
            message['user_email'] = "dont leave field empty"
        
        mobile = request.POST["mobile_no"] 
        if not mobile.isnumeric():
            message['mobile'] = "use number as your mobile no."
        if len(mobile) != 10:
            print(len(mobile))
            message['mobile'] = "enter valid mobile number"    
        if mobile == "":
            message['mobile'] = "dont leave field empty"
        if mobile.isnumeric():
            mobile = int(mobile)    
                
        age = request.POST["age"] 
        if not age.isnumeric():
            message['age'] = "use number as your age"
        if len(age) > 2:
            message['age'] = "enter valid age" 
        if age == "":
            message['age'] = "edont leave field empty"
                   
        if age.isnumeric():
            age = int(age)
        
        user_address = request.POST["address"]
        if user_address == "":
            message['user_address'] = "dont leave field empty"

        user_id = request.session['user_id']
        data = user.objects.get(user_id=user_id)
        details = {"fname":fname,"lname":lname,"user_email":user_email,"mobile":mobile,"age":age,"user_address":user_address}
        print(message)
        if bool(message):
            tournament_data = tournament.objects.filter(accepted_user = data)
            display = "block"
            display2 = "none"
            return render(request,"profile2.html",{"display2":display2,"display":display,"message" : message,"details":details,'data' : data,"tournament":tournament_data})

        gender = request.POST["gender"]
        print(gender)

        data.first_name = fname
        data.last_name = lname
        data.gender = gender
        data.address = user_address
        data.email = user_email
        data.mobile_no = mobile
        data.age = age
        data.save()
        tournament_data = tournament.objects.filter(accepted_user = data)
        display = "none"
        display2 = "block"
        return render(request, "profile2.html",{"display2":display2,'data' : data,"tournament":tournament_data,"display":display }) 

    if request.method == 'GET':  
        if request.session['user_id'] == "":
            return render(request,"home.html")  
        user_id = request.session['user_id'] 
        data = user.objects.get(user_id=user_id) 
        tournament_data = tournament.objects.filter(accepted_user = data)
        display = "none"
        display2 = "block"
        return render(request, "profile2.html",{"display2":display2,"display":display,'data' : data,"tournament":tournament_data })    


def booking_page(request): 
    if request.session['user_id'] == "":
        return render(request,"home.html") 
    user_id = request.session['user_id'] 
    user_data = user.objects.get(user_id=user_id)
    sports_list = sports.objects.all()
    booking_list = booking.objects.filter(user = user_data)
    t = date.today()
    today = str(t)
    print(today)

    data = {"today":today,"sports":sports_list,'data' : booking_list,'user' : user_data,"form_1":"block","form_2":"none"}

    return render(request,"booking.html",data)

def booking_request(request):
    if request.method == 'POST':

        start_time_list = ['null','6 am','7 am','8 am','9 am','10 am','11 am','12 am','1 pm','2 pm','3 pm','4 pm','5 pm',
        '6 pm','7 pm','8 pm','9 pm','10 pm','11 pm']

        end_time_list = ['null','7 am','8 am','9 am','10 am','11 am','12 am','1 pm','2 pm','3 pm','4 pm','5 pm','6 pm',
        '7 pm','8 pm','10 pm','11 pm','12 pm']

        user_id = request.session['user_id']

        message = {}
        some_var = request.POST.getlist('checks[]')
        if len(some_var) == 0:
            message['check'] = " select time slot "

        s_id =request.POST["sports"]
        if s_id == "select sports":
            message['sports'] = "select sports"
        if s_id != "select sports" :
            sports_id = int(s_id)

        g_id =request.POST["ground"]
        if g_id == "select group":
            message['ground'] = "select group"
        if g_id != "select group" :
            ground_id = int(g_id)

        t_id = request.POST["team"]
        if t_id == "select team":
            message['team'] = "select team"
        if t_id != "select team" :
            team_id = int(t_id)

        date = request.POST["date"]
        if date == "":
            message['date'] = "select date"
        print(message)
        if bool(message):
            user_id = request.session['user_id'] 
            user_data = user.objects.get(user_id=user_id)
            sports_list = sports.objects.all()
            booking_list = booking.objects.filter(user = user_data)
            data = {"message":message,"sports":sports_list,'data' : booking_list,'user' : user_data,"form_1":"block","form_2":"none"}
            return render(request,"booking.html",data)

        user_data = user.objects.get(user_id=user_id)
        sport_data = sports.objects.get(sports_id=sports_id)
        ground_data = ground.objects.get(ground_id=ground_id)
        team_data = team.objects.get(team_id = team_id)
        datetimeobj = datetime.strptime(date, "%Y-%m-%d")

        for i in range(0, len(some_var)):
            some_var[i] = int(some_var[i])
            
        groups = []
        for k, g in groupby(enumerate(some_var), lambda x: x[0]-x[1]):
            groups.append(list(map(itemgetter(1), g)))    

        print(len(groups))
        for i in range(0,len(groups)):
            k=len(groups[i]) - 1
            
            data = booking.objects.create(
            user=user_data,
            sports=sport_data,
            ground=ground_data,
            team=team_data,
            date=datetimeobj,
            start_time=start_time_list[groups[i][0]],
            end_time=end_time_list[groups[i][k]])
        
        sports_info = sports.objects.all()
        booking_list = booking.objects.filter(user = user_data)
        return redirect('/booking')  
    if request.method == 'GET':
        return redirect('/booking')  


@csrf_exempt          
def getPlayerList(request):
    result_set = []
    data = request.body.decode('utf-8')
    print(data)
    print(type(data))
    y = json.loads(data)
    t_id = int(y["id"])
    print(type(t_id))
    print(t_id)
    team_data = team.objects.get(team_id = t_id)
    user_data = user.objects.get(user_id = request.session['user_id'])
    player_data = player.objects.filter(Q(user = user_data) & Q(team = team_data))
    for road in player_data:
        result_set.append({'player_id': road.player_id,'name': road.name,'team_id': road.team.team_id,'team': road.team.name,'gender': road.gender})  

    print(result_set)      
    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')

def edit_player_data(request,id):
    player_id  = id
    player_data = player.objects.get(player_id = player_id)
    user_id = request.session['user_id'] 
    user_obj = user.objects.get(user_id = user_id)
    team_list = team.objects.filter(user = user_obj)
   
    add = "none"
    edit = "block"
    return render(request, "player.html",{'data' : team_list ,"player" : player_data,"add":add,"edit":edit}) 
     
@csrf_exempt          
def getground(request):
    result_set = []
    data = request.body.decode('utf-8')
    print(data)
    print(type(data))
    y = json.loads(data)
    sports_id = int(y["id"])
    sports_data = sports.objects.get(sports_id = sports_id)
    groun_list = ground.objects.filter(sports = sports_data)
    for road in groun_list:
        print("sports name", road.ground_name)
        result_set.append({'name': road.ground_name,'id': road.ground_id})  

    print(result_set)      
    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')

def makePaymentForbooking(request,id):
    time_start_dir = {'6 am':'1','7 am':'2','8 am':'3','9 am':'4','10 am':'5','11 am':'6','12 am':'7','1 pm':'8',
    '2 pm':'9','3 pm':'10','4 pm':'11','5 pm':'12','6 pm':'13','7 pm':'14','8 pm':'15','9 pm':'16','10 pm':'17','11 pm':'18'}
    time_end_dir = {'7 am':'1','8 am':'2','9 am':'3','10 am':'4','11 am':'5','12 am':'6','1 pm':'7','2 pm':'8',
    '3 pm':'9','4 pm':'10','5 pm':'11','6 pm':'12','7 pm':'13','8 pm':'14','9 pm':'15','10 pm':'16','11 pm':'17','12 pm':'18'}
    booking_id = id
    booking_record = booking.objects.get(booking_id = booking_id)
    start = int(time_start_dir[booking_record.start_time])
    end = int(time_end_dir[booking_record.end_time])+1
    count = 0
    for i in range(start, end):
        print(i)
        count= count+1

    amount = int(booking_record.ground.per_hour_charge)*count
    user_id = request.session['user_id'] 
    user_data = user.objects.get(user_id=user_id)
    client = razorpay.Client(auth=("rzp_test_YbY0MijFRNp7D8", "YU6JFHnAOBWJLtLCZELLtIVR"))
    data = { "amount":  amount*100, "currency": "INR", "payment_capture": "0" }
    payment_order = client.order.create(data=data)
    payment_order_id = payment_order['id']

    currency = 'INR'
    r_order_id = client.order.create(dict(amount=amount,
                currency=currency,receipt= payment_order_id,payment_capture='0'))
    razorpay_order_id = r_order_id['id']            
    data = payment.objects.create(
            user=user_data,
            total_amount=amount,
            order_id=payment_order_id,
            razorpay_order_id=razorpay_order_id,
            booking = booking_record

    )
    print(request.session['booking_id'])
    context = {
        'amount' : amount, 'api_key' : 'rzp_test_YbY0MijFRNp7D8', 'order_id' : payment_order_id , 'url' :'http://127.0.0.1:8000/payment_succses_handel'
    }
    return render(request, "makePayment.html",{'amount':amount,'booking' : booking_record, "data" : context,"user" : user_data})   



@csrf_exempt          
def payment_succses_handel(request):
    payment_id = request.POST.get('razorpay_payment_id','')
    order_id= request.POST.get('razorpay_order_id','')
    signature = request.POST.get('razorpay_signature','')
    param_dict = {
        'razorpay_payment_id':payment_id,
        'razorpay_order_id':order_id,
        'razorpay_signature':signature
    }
    try:
        payment_data = payment.objects.get(order_id=order_id)
    except:
        return render(request, 'payment_failed.html') 
    payment_data.razorpay_payment_id = payment_id
    payment_data.razorpay_signature_id = signature
    payment_data.save()     
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)) 
    result = client.utility.verify_payment_signature(param_dict)
    booking_data = booking.objects.get(booking_id = payment_data.booking.booking_id)
    today = date.today()
  
    try:
        if result:
            amount = payment_data.total_amount
            payment_data.status = 1
            payment_data.date=date.today()
            print("seccess")
            booking_data.status = True
            booking_data.save()
            payment_data.payment_for = 1
            payment_data.save()
            return render(request, 'payment_seccess.html')
        else:
            payment_data.status = 2
            payment_data.save()
            return render(request, 'payment_failed.html')    
    except: 
        payment_data.status = 2
        payment_data.save()
        return render(request, 'payment_failed.html') 

@csrf_exempt          
def gettime(request):
    time_start_dir = {'6 am':'1','7 am':'2','8 am':'3','9 am':'4','10 am':'5','11 am':'6','12 am':'7','1 pm':'8',
    '2 pm':'9','3 pm':'10','4 pm':'11','5 pm':'12','6 pm':'13','7 pm':'14','8 pm':'15','9 pm':'16','10 pm':'17','11 pm':'18'}
    time_end_dir = {'7 am':'1','8 am':'2','9 am':'3','10 am':'4','11 am':'5','12 am':'6','1 am':'7','2 pm':'8',
    '3 pm':'9','4 pm':'10','5 pm':'11','6 pm':'12','7 pm':'13','8 pm':'14','9 pm':'15','10 pm':'16','11 pm':'17','12 pm':'18'}
    result_set = []
    data = request.body.decode('utf-8')
    y = json.loads(data)
    gound_id = int(y["id"])
    print(gound_id)
    date = y["date"]
    datetimeobj = datetime.strptime(date, "%Y-%m-%d")
    print(date)
    print(type(datetimeobj))
    groumd_data = ground.objects.get(ground_id = gound_id)
    booked = booking.objects.filter(Q(date=datetimeobj) & Q(ground = groumd_data))
    for road in booked:
        start = int(time_start_dir[road.start_time])
        end = int(time_end_dir[road.end_time])+1
        for i in range(start, end):
            result_set.append({'id': i})  

    print(result_set)      
    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')

def player_page(request):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    user_id = request.session['user_id'] 
    user_obj = user.objects.get(user_id = user_id)
    team_list = team.objects.filter(user = user_obj)
    data = player.objects.filter(user = user_obj).order_by('team')
    add = "block"
    edit = "none"
    return render(request, "player.html",{'data' : team_list ,"player" : data,"add":add,"edit":edit}) 

def add_player(request):
    if request.method == "POST":

        player_name = request.POST["name"]
        player_gender = request.POST["gender"]
        team_id = int(request.POST["team"])
        user_id = request.session['user_id'] 
        user_data = user.objects.get(user_id = user_id)
        team_data = team.objects.get(team_id = team_id)
        player_list = player.objects.filter(user_id = user_id)
        team_list = team.objects.filter(user = user_data)

        if player_name == "":
            message = "dont leave field empty"
            print(message)
            add = "block"
            edit = "none"
            return render(request, "player.html",{'message':message, 'data' : team_list , 'player' : player_list,"add":add,"edit":edit})

        insert = player.objects.create(
        user = user_data,
        team = team_data,
        name = player_name,
        gender = player_gender,
         )
        insert.save()
        add = "block"
        edit = "none"
        
        return render(request, "player.html",{'data' : team_list , 'player' : player_list,"add":add,"edit":edit})  
    if request.method == "GET":
        if request.session['user_id'] == "":
            return render(request,"home.html")
        user_id = user_id = request.session['user_id'] 
        user_data = user.objects.get(user_id = user_id)
        player_list = player.objects.filter(user = user_data)
        team_list = team.objects.filter(user = user_data)
        add = "block"
        edit = "none"
        return render(request, "player.html",{'data' : team_list , 'player' : player_list,"add":add,"edit":edit})  


def update_player(request):
    if request.method == "POST":
        player_name = request.POST["name2"]
        player_gender = request.POST["gender2"]
        team_id = int(request.POST["team2"])
        player_id = int(request.POST["player_id2"])
        user_id = request.session['user_id'] 
        player_data = player.objects.get(player_id = player_id)
        user_data = user.objects.get(user_id = user_id)
        team_data = team.objects.get(team_id = team_id)
        player_list = player.objects.filter(user_id = user_id)
        team_list = team.objects.filter(user = user_data)

        if player_name == "":
            add = "none"
            edit = "block"
            message = "enter player name"
            return render(request, "player.html",{'player_id2':player_id,'data' : team_list , 'player' : player_list,"add":add,"edit":edit,"error":message})

        player_data.name = player_name
        player_data.team = team_data
        player_data.gender = player_gender
        player_data.save()
        add = "none"
        edit = "block"
        return render(request, "player.html",{'data' : team_list , 'player' : player_list,"add":add,"edit":edit})  
    if request.method == "GET":
        if request.session['user_id'] == "":
            return render(request,"home.html")
        user_id = user_id = request.session['user_id'] 
        user_data = user.objects.get(user_id = user_id)
        player_list = player.objects.filter(user = user_data)
        team_list = team.objects.filter(user = user_data)
        add = "none"
        edit = "block"
        return render(request, "player.html",{'data' : team_list , 'player' : player_list,"add":add,"edit":edit})

def delete_player(request,id):
    player_id = id
    print(player_id)
    player_record = player.objects.get(player_id = player_id)
    player_record.delete()
    user_id = user_id = request.session['user_id'] 
    data = player.objects.filter(user_id = user_id)
    return redirect('/player') 

def team_page(request):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    user_id = request.session['user_id']
    user_data = user.objects.get(user_id = user_id)
    team_list = team.objects.filter(user = user_data)
    sports_list = sports.objects.all()
    add = "block"
    edit = "none"
    return render(request, "team_page.html",{'data' : team_list,'sports' : sports_list,"add":add,"edit":edit})  
        
def team_add(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        if team_name == "":
            message = "enter team name"
            user_data = user.objects.get(user_id = user_id)
            team_list = team.objects.filter(user = user_data)
            sport_list = sports.objects.all()
            add = "block"
            edit = "none"
            return render(request, "team_page.html",{"add":add,"edit":edit,'data' : team_list,"message":message,'sports' : sport_list}) 

        sports_id = request.POST["sports"]
        sport_data = sports.objects.get(sports_id= sports_id)
        
        data = team(user = user_data,name = team_name, sports=sport_data)
        data.save()
        team_list = team.objects.filter(user = user_data)
        add = "block"
        edit = "none"
        sport_list = sports.objects.all()
        return render(request, "team_page.html",{"add":add,"edit":edit,'data' : team_list,'sports' : sport_list})  
    if request.method == "GET":
        if request.session['user_id'] == "":
            return render(request,"home.html")
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        team_list = team.objects.filter(user = user_data)
        sport_list = sports.objects.all()
        add = "block"
        edit = "none"
        return render(request, "team_page.html",{"add":add,"edit":edit,'data' : team_list,'sports' : sport_list})

def update_team(request):
    if request.method == "POST":
        team_name = request.POST["team_name2"]
        sports_id = request.POST["sports2"]
        team_id = int(request.POST["team_id2"])
        sport_data = sports.objects.get(sports_id= sports_id)
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        team_data = team.objects.get(team_id = team_id)
        if team_name == "":
            message = "enter team name"
            user_data = user.objects.get(user_id = user_id)
            team_list = team.objects.filter(user = user_data)
            sport_list = sports.objects.all()
            add = "none"
            edit = "block"
            return render(request, "team_page.html",{"team_id":team_id,"add":add,"edit":edit,'data' : team_list,"message2":message,'sports' : sport_list}) 

        team_data.name = team_name
        team_data.sports = sport_data
        team_data.save()
        print(team_data.name)
        team_list = team.objects.filter(user = user_data)
        sports_list = sports.objects.all()
        add = "none"
        edit = "block"
        return render(request, "team_page.html",{"add":add,"edit":edit,'data' : team_list,'sports' : sports_list})  
    if request.method == "GET":
        if request.session['user_id'] == "":
            return render(request,"home.html")
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        team_list = team.objects.filter(user = user_data)
        sports_list = sports.objects.all()
        add = "none"
        edit = "block"
        return render(request, "team_page.html",{"add":add,"edit":edit,'data' : team_list,'sports' : sports_list})

def delete_team(request,id):
    team_id = id
    print(team_id)
    team_record = team.objects.get(team_id = team_id)
    team_record.delete()
    return redirect('/team_page')

def tournament_page(request):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    sports_list = sports.objects.all()
    user_id = request.session['user_id']
    print(user_id)
    user_data = user.objects.get(user_id = user_id)
    tournament_data = tournament.objects.filter(created_by = user_data)

    return render(request, "tournament_page.html",{'data' : sports_list,'data2' : tournament_data}) 

def tournament_accept(request,id):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    tournament_id = id
    tournament_data = tournament.objects.get(tournament_id = tournament_id)
    tournament_data.response = "accepted"
    tournament_data.save()
    return redirect('/profile2')

def tournament_reject(request,id):
    if request.session['user_id'] == "":
        return render(request,"home.html")
    tournament_id = id
    tournament_data = tournament.objects.get(tournament_id = tournament_id)
    tournament_data.response = "rejected"
    tournament_data.save()
    return redirect('/profile2')    

def class_page(request):
    classes_details = classes.objects.all()
    return render(request, "class_page.html",{'data' : classes_details})  
    
def payment_test(request):
    client = razorpay.Client(auth=("rzp_test_YbY0MijFRNp7D8", "YU6JFHnAOBWJLtLCZELLtIVR"))
    data = { "amount": 10000, "currency": "INR", "payment_capture": "0" }
    payment_order = client.order.create(data=data)
    payment_order_id = payment_order['id']
    context = {
        'amount' : 100, 'api_key' : 'rzp_test_YbY0MijFRNp7D8', 'order_id' : payment_order_id,'url':'http://127.0.0.1:8000/payment_succses_handel'
    }
    return render(request,'pay.html',context)       

        
def buy_pack(request,id):
    class_data = classes.objects.get(classes_id = id)
    user_data = user.objects.get(user_id=request.session['user_id'])
    amount=class_data.price
    client = razorpay.Client(auth=("rzp_test_YbY0MijFRNp7D8", "YU6JFHnAOBWJLtLCZELLtIVR"))
    data = { "amount":  amount*100, "currency": "INR", "payment_capture": "1" }
    payment_order = client.order.create(data=data)
    payment_order_id = payment_order['id']
    currency = 'INR'
    r_order_id = client.order.create(dict(amount=amount,
                currency=currency,receipt= payment_order_id,payment_capture='0'))
    razorpay_order_id = r_order_id['id']            
    data = payment.objects.create(
            user=user_data,
            total_amount=amount,
            order_id=payment_order_id,
            razorpay_order_id=razorpay_order_id,
            classes = class_data,
            payment_for=2

    )            

    context = {
        'amount' : class_data.price, 'api_key' : 'rzp_test_YbY0MijFRNp7D8', 'order_id' : payment_order_id , 'url':'http://127.0.0.1:8000/handle_class_pay'
    }
    return render(request, "buy_pack.html",{'data' : class_data,'context':context, 'user' : user_data})  

@csrf_exempt        
def handle_class_pay(request):
    payment_id = request.POST.get('razorpay_payment_id','')
    order_id= request.POST.get('razorpay_order_id','')
    signature = request.POST.get('razorpay_signature','')
    param_dict = {
        'razorpay_payment_id':payment_id,
        'razorpay_order_id':order_id,
        'razorpay_signature':signature
    }
    try:
        payment_data = payment.objects.get(order_id=order_id)
    except:
        return render(request, 'payment_failed.html') 
    payment_data.razorpay_payment_id = payment_id
    payment_data.razorpay_signature_id = signature
    payment_data.save()     
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)) 
    result = client.utility.verify_payment_signature(param_dict)
    today = date.today()
  
    try:
        if result:
            payment_data.status = 1
            payment_data.date=date.today()
            payment_data.save()
            return render(request, 'payment_seccess.html')
        else:
            payment_data.status = 2
            payment_data.save()
            return render(request, 'payment_failed.html')    
    except:  
        payment_data.status = 2
        payment_data.save()
        return render(request, 'payment_failed.html') 


@csrf_exempt          
def getteams(request):
    result_set = []
    data = request.body.decode('utf-8')
    print(data)
    print(type(data))
    y = json.loads(data)
    sports_id = int(y["id"])
    user_id = request.session['user_id']
    user_data = user.objects.get(user_id=user_id)
    sports_data = sports.objects.get(sports_id = sports_id)
    team_data = team.objects.filter(Q(sports=sports_data) & Q(user=user_data))
    for road in team_data:
        result_set.append({'name': road.name,'id': road.team_id})  
    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')

@csrf_exempt          
def getTeamForrequist(request):
    result_set = []
    data = request.body.decode('utf-8')
    print(data)
    print(type(data))
    y = json.loads(data)
    sports_id = int(y["id"])
    sports_data = sports.objects.get(sports_id = sports_id)
    user_data = user.objects.get(user_id=request.session['user_id'])
    team_data = user.objects.filter(Q(sports = sports_data) & Q(user=user))
    for road in team_data:
        result_set.append({'name': road.name,'id': road.team_id})  

    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')

def pop_up(request):
    return render(request, "popup.html")  

def add_tournament(request):
    if request.method == 'POST' :
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        
        message = {}
        name = request.POST['title']
        if name == "":
            message['name'] = " please enter title "

        s_id = request.POST['sports']
        if s_id == "select sport":
            message['sport'] = " please select sports "
        if s_id != "select sport":
            sports_id = int(s_id) 
            sports_data = sports.objects.get(sports_id = sports_id)   
      
        t_id = request.POST['team']
        if t_id == "select team":
            message['team'] = " please select team "
        if t_id != "select team":
            team_id = int(t_id)
            team_data = team.objects.get(team_id = team_id)

        is_private = request.POST.get('checks', True)
        if not is_private:
            message['user'] = " please select user "
        else:
            other_user = int(is_private)    

        detail =  request.POST['detail']
        if detail == "":
            message['detail'] = " please enter details "

        sports_list = sports.objects.all()
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        tournament_data = tournament.objects.filter(created_by = user_data)    

        if bool(message):
            return render(request, "tournament_page.html",{'message':message,'data' : sports_list,'data2' : tournament_data}) 

        other_user_data = user.objects.get(user_id = other_user)

        tournament.objects.create(
            name = name,
            sports = sports_data,
            created_by = user_data,
            team_1 = team_data,
            accepted_user = other_user_data,
            team_2 = None,
            booking = None,
            details = detail
        )

        return render(request, "tournament_page.html",{'data' : sports_list,'data2' : tournament_data}) 
 
    if request.method == 'GET':
        if request.session['user_id'] == "":
            return render(request,"home.html")
        sports_list = sports.objects.all()
        user_id = request.session['user_id']
        user_data = user.objects.get(user_id = user_id)
        tournament_data = tournament.objects.filter(created_by = user_data)

        return render(request, "tournament_page.html",{'data' : sports_list,'data2' : tournament_data}) 

def booking_request_tournamate(request,id,s_id): 
    if request.session['user_id'] == "":
        return render(request,"home.html") 
    request.session['booking_for_tournamate'] = id
    user_data = user.objects.get(user_id = request.session['user_id'])
    sports_data = sports.objects.get(sports_id = s_id)
    ground_list = ground.objects.filter(sports = sports_data)
    team_data = team.objects.filter(Q(user=user_data) & Q(sports=sports_data))
    sports_name = sports_data.sports_name
    sports_id = sports_data.sports_id
    booking_list = booking.objects.filter(user = user_data)
    t = date.today()
    today = str(t)
    return render(request, "booking.html",{"today2":today,"s_id":s_id,"form_1":"none","form_2":"block","team":team_data,"ground":ground_list,"disabled":"disabled","sports_name":sports_name,"sports_id":sports_id,'data' : booking_list,'user' : user_data}) 

@csrf_exempt          
def user_for_tournament(request):
    result_set = []
    data = request.body.decode('utf-8')
    y = json.loads(data)
    sports_id = int(y["id"])
    sports_data = sports.objects.get(sports_id = sports_id)
    team_data = team.objects.filter(sports = sports_data).distinct()
    user_id = request.session['user_id']

    temp = []
    res = dict()
   
    for road in team_data:
        if road.user.user_id != user_id:
            if road.user.user_id not in temp:
                temp.append(road.user.user_id)
                result_set.append({'name': road.name,'id': road.team_id,'fname':road.user.first_name,
        'lname':road.user.last_name,'user_id':road.user.user_id})  

    json_string = json.dumps(result_set)
    return HttpResponse(json_string, content_type='application/json')


def booking_turnament(request):
    if request.method == 'POST':
        time_slot = []
        start_time_list = ['null','6 am','7 am','8 am','9 am','10 am','11 am','12 am','1 pm','2 pm','3 pm','4 pm','5 pm',
        '6 pm','7 pm','8 pm','9 pm','10 pm','11 pm']

        end_time_list = ['null','7 am','8 am','9 am','10 am','11 am','12 am','1 pm','2 pm','3 pm','4 pm','5 pm','6 pm',
        '7 pm','8 pm','10 pm','11 pm','12 pm']

        some_var = request.POST.getlist('checks2[]')
        message = {}
        if len(some_var) == 0:
            message['check2'] = " select time slot "

        date = request.POST["date2"]
        if date == "" :
            message['date2'] = " select date "

        s_id = request.POST["s_id"]    

        if bool(message):  
            user_data = user.objects.get(user_id = request.session['user_id'])
            sports_data = sports.objects.get(sports_id = s_id)
            ground_list = ground.objects.filter(sports = sports_data)
            team_data = team.objects.filter(Q(user=user_data) & Q(sports=sports_data))
            sports_name = sports_data.sports_name
            sports_id = sports_data.sports_id
            booking_list = booking.objects.filter(user = user_data)

            return render(request, "booking.html",{"message":message,"form_1":"none","form_2":"block","team":team_data,"ground":ground_list,"disabled":"disabled","sports_name":sports_name,"sports_id":sports_id,'data' : booking_list,'user' : user_data}) 
  
        user_id = request.session['user_id']
        sports_id =int(request.POST["sports2"])
        ground_id =int(request.POST["ground2"])
        team_id =int(request.POST["team2"])
        
        user_data = user.objects.get(user_id=user_id)
        sport_data = sports.objects.get(sports_id=sports_id)
        ground_data = ground.objects.get(ground_id=ground_id)
        team_data = team.objects.get(team_id = team_id)
        datetimeobj = datetime.strptime(date, "%Y-%m-%d")

        for i in range(0, len(some_var)):
            some_var[i] = int(some_var[i])
            
        groups = []
        for k, g in groupby(enumerate(some_var), lambda x: x[0]-x[1]):
            groups.append(list(map(itemgetter(1), g)))    

        print(len(groups))
        print(groups)
        if len(groups) == 1:
            k=len(groups[0]) - 1
            print("valide")
            data = booking.objects.create(
            user=user_data,
            sports=sport_data,
            ground=ground_data,
            team=team_data,
            date=datetimeobj,
            start_time=start_time_list[groups[0][0]],
            end_time=end_time_list[groups[0][k]])
            data.save()

            booking_record = booking.objects.get(booking_id = data.booking_id)
            tournament_id = request.session['booking_for_tournamate']
            tournament_data = tournament.objects.get(tournament_id = tournament_id)
            tournament_data.booking = booking_record
            tournament_data.team = team_data
            tournament_data.status = True
            tournament_data.save()
            request.session['booking_for_tournamate'] = ""
            
        sports_info = sports.objects.all()
        booking_list = booking.objects.filter(user = user_data)
        return redirect('/booking')  
    if request.method == 'GET':
        return redirect('/booking')  
 

def forgot_page(request): 

    return render(request, "forgot_pass_page.html")



def forgot_email(request): 
    if request.method == "POST":
        email = request.POST['email']
        user_data = user.objects.get(email = email)
        if not user_data:
            return redirect('/home')
        token = str(uuid4())   
        send_email_pass_forgot(user_data, token)  
        user_data.email_token = token
        user_data.save()
        return render(request, "sent_pass_email.html")
    if request.method == "GET":
        return render(request, "sent_pass_email.html")


def change_pass(request,token): 
    print(token)
    user_data = user.objects.get(email_token = token)
    if user_data:
        return render(request, "change_pass_page.html",{'user_id':user_data.user_id})

def change_pass_logic(request): 
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']  

    user_id = int(request.POST['u_id'])
    if pass1 == pass2 :
        user_data = user.objects.get(user_id = user_id)
        user_data.password = pass1
        user_data.email_token = "none"
        user_data.save()
        
    return render(request, "pass_changed_page.html")


def send_email_to_user(request,id):
    creater_user = id
    creater_data = user.objects.get(user_id = creater_user)
    first_name = creater_data.first_name
    last_name = creater_data.last_name
    return render(request, "send_email_to_user.html",{'user_id':creater_user,'first_name':first_name,'last_name':last_name})

def inquiry_email(request):
     if request.method == "POST":
        creater_id = int(request.POST['user_id'])
        message = request.POST['message']
        print(message)
        creater_user = user.objects.get(user_id = creater_id)
        email = creater_user.email
        subject = " email from user of sports club "
        message = f""+message
        user_data = user.objects.get(user_id = request.session['user_id'])
        email_from = user_data.email
        recepient_list = [email]
        send_mail(subject,message,email_from,recepient_list)
        return redirect('/profile2') 
    






















































