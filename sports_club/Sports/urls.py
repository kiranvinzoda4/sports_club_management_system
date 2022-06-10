"""sports_club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views 

from django.contrib import admin
from django.urls import path
from Sports import views



urlpatterns = [
    
    path('', views.home, name='home'),
    path('login', views.login, name='submit'),
    path('register_user', views.register_user, name='register_user'),  
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('uptade_profile',views.uptade_profile,name='uptade_profile'),
    path('booking', views.booking_page, name='booking'),
    path('booking_request', views.booking_request, name='booking_request'),
    path('getground', views.getground, name='getground'),
    path('player', views.player_page, name='load_add_player_page'),
    path('add_player', views.add_player, name='add_player'),
    path('update_player', views.update_player, name='update_player'),
    path('delete_player/<int:id>', views.delete_player, name='delete_player'),
    path('profile2',views.profile2,name='profile'),
    path('team_page',views.team_page,name='team_page'),
    path('team_add',views.team_add,name='team_page'),
    path('update_team',views.update_team,name='update_team'),
    path('delete_team/<int:id>', views.delete_team, name='delete_team'),
    path('tournament',views.tournament_page,name='tournament_page'),
    path('class',views.class_page,name='class_page'),
    path('logout',views.logout,name='class_page'),
    path('pay',views.payment_test,name='class_page'),
    path('getPlayerList',views.getPlayerList,name='getPlayerList'),
    path('edit_player_data/<int:id>', views.edit_player_data, name='edit_player_data'),
    path('payment_succses_handel',views.payment_succses_handel,name='payment_succses_handel'),

    path('home',views.home,name='class_page'),
    path('login_page',views.login_page,name='login_page'),
    path('registration_page',views.registration_page,name='registration_page'),
    path('about_us',views.about_us,name='class_page'),
    path('contact_us',views.contact_us,name='class_page'),
    
    path('active_user/<token>/', views.active_user, name='active_user'),
    
    path('buy_pack/<int:id>', views.buy_pack, name='buy_pack'),
    path('handle_class_pay', views.handle_class_pay, name='handle_class_pay'),
    path('getteams', views.getteams, name='getteams'),
    path('getTeamForrequist', views.getTeamForrequist, name='getTeamForrequist'),

    path('pop_up', views.pop_up, name='buy_pack'),
    
    path('gettime', views.gettime, name='gettime'),

    path('makePaymentForbooking/<int:id>',views.makePaymentForbooking,name='makePaymentForbooking'),

    path('add_tournament',views.add_tournament,name='add_tournament'),

    path('booking_turnament',views.booking_turnament,name='booking_turnament'),
    path('user_for_tournament',views.user_for_tournament,name='user_for_tournament'),
    path('booking_request_tournamate/<int:id>/<int:s_id>', views.booking_request_tournamate, name='booking_request_tournamate'),
    path('tournament_accept/<int:id>', views.tournament_accept, name='tournament_accept'),
    path('tournament_reject/<int:id>', views.tournament_reject, name='tournament_reject'),
    path('forgot_page', views.forgot_page, name='forgot_page'),
    path('forgot_email', views.forgot_email, name='forgot_email'),
    
    path('change_pass/<token>/', views.change_pass, name='change_pass'),
    path('change_pass_logic', views.change_pass_logic, name='change_pass_logic'),
    path('send_email_to_user/<int:id>', views.send_email_to_user, name='send_email_to_user'),
    path('inquiry_email', views.inquiry_email, name='inquiry_email'),


]
