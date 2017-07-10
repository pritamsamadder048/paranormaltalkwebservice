from django.shortcuts import render




from django.http import HttpResponse



import datetime
import urllib
from urllib.request import urlopen




from  django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import  Response
from  rest_framework import  status
from rest_framework import generics
from rest_framework import views



import json
import sys,os
import datetime
from datetime import date


from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage

import math



from .models import  UserDetail
from .serializers import UserDetailSerializer

from .models import UserSession
from .models import Post
from .serializers import PostSerializer
from .models import Following
from .serializers import FollowingSerializer



# register the user
class RegisterUser(APIView):

    def post(self,request):

        signup_data = {}
        responsedata={}

        try:

            print("trying to register",request.POST)

            for key in request.POST:

                signup_data[key] = request.POST[key].strip()
            print("sign up data : ",signup_data)

            try:
                if ( (not signup_data['email']) or (not signup_data['name']) or (not signup_data['gender'])  or (not signup_data['password']) ):

                    #print("not all data",responsedata)

                    print(signup_data)

                    responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                    print(responsedata)

                    return Response(responsedata)
            except:

                #print("not all data except ","   ", responsedata)

                print(signup_data)

                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                return Response(responsedata)


            try:
                ud = UserDetail.objects.get(email=signup_data['email'])
                if (ud):
                    responsedata={"successstatus":"error","message":"the email is already registered.Please login ."}
                    return Response(responsedata)

            except UserDetail.DoesNotExist:

                pass


            try:


                print("in block")

                ud = UserDetail()
                print("init")
                ud.full_name = signup_data['name']

                if signup_data.get('mobile',None) is not None:

                    ud.mobile = signup_data["mobile"]
                
                ud.email = signup_data['email']
                ud.set_password(signup_data['password'])
                ud.gender=signup_data['gender'] 

                print("trying to save data")

                ud.save()
                print("user details : ",ud)

                fd=Following()
                fd.user_id=ud.user_id
                fd.userdetail_ref=ud
                fd.user_full_name=ud.full_name
                fd.following_id=ud.user_id
                fd.followingdetail_ref=ud
                fd.following_full_name=ud.full_name
                fd.save()



                #s=sendverificationlink_fun(ud.id)

                #print("sending email...")


                #if (s==0):


                 #   print("success fully sent email")


                responsedata={"successstatus":"ok","message":"successfully registered.now login to continue"}
                print(responsedata)
                return Response(responsedata)
                #else:


                #    print("error occured trying to send email")

                #    responsedata = {"successstatus": "error", "message": "error occured.could not send the email."}
                #    return Response(responsedata)

            except Exception as e:

                print("in inner except : ",e)
                responsedata = {"successstatus": "error", "message": "unknown error. Please try again"}
                return Response(responsedata)



        except Exception as e:


            print("in outer except")
            print("Signup Error : ",e)
            responsedata = {"successstatus": "error", "message": "unknown error. Please try again"}
            return Response(responsedata)






class Login(APIView):

    def post(self,request):

        login_data = {}

        #print("trying login")




        try:

            if( request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey=request.POST['user_session_key']


            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):
                    print("sessionfound")
                    try:
                        del request.session['user_session_key']
                    except:
                        pass
                    try:
                        us.delete()
                    except:
                        pass
            except UserSession.DoesNotExist:
                try:
                    del request.session['user_session_key']
                except:
                    pass
                pass
        except:
            print("no session found")


            try:
                del(request.session['user_session_key'])
            except:
                pass

            try:
                us.delete()
            except:
                pass




        for key in request.POST:
            login_data[key] = request.POST[key].strip()

        print("login post : ",request.POST)
        print("login data :",login_data)

        try:
            if((not login_data['email']) or (not login_data['password'])):


                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print("if not data",responsedata)
                return Response(responsedata)

        except:

            responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
            print("except not data", responsedata)
            return Response(responsedata)

        try:

            ud = UserDetail.objects.get(email=login_data['email'])
            # bodytext+="<p>user data available</p>"

            correctpassword = ud.check_password(login_data['password'])
            # bodytext+="<p>"+str(correctpassword)+"</p>"

            if (correctpassword):

                try:
                    print("correct password")
                    us = UserSession.objects.get(email=ud.email)
                    uskey = us.UserSession_key
                    request.session['user_session_key'] = uskey
                    print("session available reinitialising the session")

                    #responsedata={"userid":ud.id,"user_type":ud.user_type,"areapincode":ud.pincode,'user_session_key':us.UserSession_key}
                    sud=UserDetailSerializer(ud)
                    responsedata = {"userdetail": sud.data,"successstatus":"ok","message":"successfully logged in",'user_session_key': us.UserSession_key}
                    print("after correct ",responsedata)

                    return Response(responsedata)

                except:
                    try:
                        print("No sessinon Available..creating new session..")
                        us.delete()
                    except:
                        pass

                us = UserSession()
                us.full_name = ud.full_name
                if ud.mobile:
                    us.mobile = ud.mobile
                us.email=ud.email
                us.set_sessionkey()
                uskey = us.UserSession_key  # session key for the user
                us.UserDetail_id = ud.id
                us.UserDetail_ref = ud
                us.save()
                request.session['user_session_key'] = uskey
                sud=UserDetailSerializer(ud)

                responsedata = {"userdetail": sud.data,"successstatus":"ok","message":"successfully logged in", 'user_session_key': us.UserSession_key}
                print("New Login : ",responsedata)
                fresponse=Response(responsedata)
                fresponse.set_cookie('user_session_key', uskey)
                return fresponse
            else:
                responsedata={"successsatus":"error","message":"Email and password does not match"}
                return Response(responsedata)

        except UserDetail.DoesNotExist:

            try:

                del request.session['username']
            except:
                pass
            try:
                us.delete()
            except:
                pass

            responsedata = {"successstatus": "error", "message": "your Email is not registered. please signup"}
            return Response(responsedata)

        except :

                try:

                    del request.session['username']
                except:
                    pass
                try:
                    us.delete()
                except:
                    pass

                responsedata = {"successstatus": "error", "message": "Unknown error occured. Please try again"}

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(True, exc_type, fname, exc_tb.tb_lineno)
                return Response(responsedata)





class Logout(APIView):

    def post(self,request):

        logout_data={}
        responsedata={}

        try:

            if( request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey=request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):
                    try:
                        del request.session['user_session_key']
                    except:
                        pass
                    try:
                        us.delete()
                        responsedata={"successstatus":"ok","message":"you have successfully Logged out"}
                        return  Response(responsedata)
                    except:
                        responsedata = {"successstatus": "error", "message": "Could not process your request"}
                        return Response(responsedata)

            except UserSession.DoesNotExist:
                try:
                    del request.session['user_session_key']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:
            responsedata = {"successstatus": "error", "message": "You are not logged in"}
            return Response(responsedata)







