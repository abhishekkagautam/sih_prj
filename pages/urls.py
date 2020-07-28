from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('add',views.add,name='add'),
    path('index_views',views.index_views,name='index_views'),
    #path('mark',views.mark,name='mark'),
    path('signup',views.signup,name='signup')

]