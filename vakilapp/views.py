from django.shortcuts import render,redirect,HttpResponse
from vakilapp.models import *
from datetime import datetime,time,timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def send_email(subject,message,recipient_list):

    email_from = 'evakeel.website@gmail.com'
    send_mail(subject, message, email_from, recipient_list)


def push_noti(Section_name,noti_text,noti_url):

    nt=notification(Section_name=Section_name,noti_text=noti_text,noti_url=noti_url,Date=datetime.today())
    nt.save()


# Create your views here.
def index(request):

    client_ip = request.META.get('REMOTE_ADDR')

    if not IPAddress.objects.exists():
        ip_address_instance = IPAddress(ip_address=client_ip,timestamp=datetime.today().date())
        ip_address_instance.save()

    for i in IPAddress.objects.all():

        if not i.ip_address==client_ip:
            ip_address_instance = IPAddress(ip_address=client_ip,timestamp=datetime.today().date())
            ip_address_instance.save()


    team=Team_Member.objects.all()
    top_blog=Blog.objects.all().order_by('-views_count')[:2]
    apts=Appointment_schedule.objects.all()

    for j in Appointment.objects.all():   
        
        if j.Date == datetime.today().date():

            apts=apts.exclude(id=j.schedule.id)


    context={'team':team,'apts':apts,'top_blog':top_blog}
    return render(request,"index.html",context)


    
def book_appointment(request):

    book=None
    
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        Subject= request.POST.get('subject')
        schedule_id = request.POST.get('schedule')

        schedule = Appointment_schedule.objects.get(pk=schedule_id)

        if not Appointment.objects.exists():

                
            apt=Appointment(Name=Name,Email=Email, Phone= Phone,Subject=Subject,schedule=schedule,Date=datetime.today())
            apt.save()

            crt_noti=Appointment.objects.order_by('-id').first()
            Section_name="Appointment"
            noti_text=str(Name)+" is booked slot of "+str(schedule.sc_name)
            noti_url="/Appointment_section#"+str(crt_noti.id)

            push_noti(Section_name,noti_text,noti_url)
            return redirect('/')

        for i in Appointment.objects.all():

            obj_date=str(i.Date)
            if int(schedule_id)== i.schedule.id and obj_date == str(datetime.today().date()):
                book=False
                break


            else:
                book=True


        if book==False:
            
           return HttpResponse('<script>alert("Enter time slot is booked"); window.location.href = "/";</script>')


        else:

            apt=Appointment(Name=Name,Email=Email, Phone= Phone,Subject=Subject,schedule=schedule,Date=datetime.today())
            apt.save()

            crt_noti=Appointment.objects.order_by('-id').first()
            Section_name="Appointment"
            noti_text=str(Name)+" is booked slot of "+str(schedule.sc_name)
            noti_url="/Appointment_section#"+str(crt_noti.id)

            push_noti(Section_name,noti_text,noti_url)

            subject = 'Appointment Confirmation: '+str(datetime.today().date())
            message = '''Dear '''+str(Name)+''',

Thank you for scheduling an appointment with us. We're looking forward to meeting you!

Here are the details of your appointment on '''+str(datetime.today().date())+'''

Date: '''+str(datetime.today().date())+'''
Start Time: '''+str(schedule.start_time)+'''
End Time: '''+str(schedule.end_time)+'''
Time Slot Name: '''+str(schedule.sc_name)+'''
Should you have any questions or need to reschedule, please feel free to get in touch with us.

We appreciate your trust in us and can't wait to assist you further.

Warm regards,
-Team E-Vakeel'''
        


        recipient_list = []
        recipient_list.append(str(Email))

        send_email(subject,message,recipient_list)


        return redirect('/')


    return render(request,"index.html")


def send_msg(request):

    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        Subject= request.POST.get('subject')
        Message=request.POST.get('message')

        user=customer(Name=Name,Email=Email, Phone= Phone,Subject=Subject,Message=Message,Date=datetime.today())
        user.save()

        crt_noti=customer.objects.order_by('-id').first()
        Section_name="Messages"
        noti_text="New contact message from "+str(Name)
        noti_url="/admin_msg#"+str(crt_noti.id)

        push_noti(Section_name,noti_text,noti_url)

    return redirect('index')

def sub_blog(request):

    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')

        for i in blog_subscribers.objects.all():

            if Email==i.Email:
                return HttpResponse('<script>alert("This given email was already taken"); window.location.href = "/";</script>')
                
         
        user=blog_subscribers(Name=Name,Email=Email,Date=datetime.today())
        user.save()


        subject = 'Welcome to E-vakeel Blogs - Your Guide to Indian Laws!'
        message = '''Dear '''+str(Name)+''',

Thank you for subscribing to E-Vakeel Blogs! 🎉
    We're excited to have you on board as we explore the fascinating world of Indian laws together.

Here's what you can expect:

1.Insightful Analysis: Dive into articles dissecting various Indian legal topics.
2.Timely Updates: Stay informed about the latest legal developments.
3.Practical Tips: Get advice on navigating legal matters effectively.
4.Exclusive Content: Access interviews, Q&A sessions, and more.

If you have any questions or suggestions, feel free to reach out!

Welcome to the community!

-Team E-Vakeel'''
        


        recipient_list = []
        recipient_list.append(str(Email))

        send_email(subject,message,recipient_list)

    return redirect('index')



def blog_menu(request):

    blog_qs=Blog.objects.all()

    result=None
    data=None
    
    if blog_qs:
        if request.GET.get('Search'):
            blog_qs=blog_qs.filter(Title__icontains=request.GET.get('Search'))
            data=request.GET.get('Search')[0:7]
            result=True
            
        if not blog_qs:
            data=request.GET.get('Search')[0:7]
            result=False
            
    context={'blog_qs':blog_qs,'result':result,"data":data}
    return render(request,"blog_menu.html",context)


def blog_temp(request,id):
     

    client_ip = request.META.get('REMOTE_ADDR')
    Blg_id= Blog.objects.get(pk=id)
    cmts=comment.objects.filter(reply_blog__id=id)[::-1]
    top_blogs=Blog.objects.all().order_by('-views_count')

    ip_address_instance = IPAddress_blog(ip_address=client_ip,timestamp=datetime.today().date(),Blog_id=Blg_id)
    ip_address_instance.save()

    got_id=Blog.objects.get(id=id)
    got_id.views_count=IPAddress_blog.objects.filter(Blog_id__id=id).count()
    got_id.comment_count=comment.objects.filter(reply_blog__id=id).count()
    got_id.save()



    context={
            'got_id':got_id,
            'cmts':cmts,
            'cmt_count':got_id.comment_count,
            'top_blogs':top_blogs
            }
    return render(request,"blog_temp.html",context)


def blog_comment(request,id):


    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        comment_text=request.POST.get('comment_text')
        reply_blog = Blog.objects.get(pk=id)

        cmt=comment(Name=Name,comment_text=comment_text,Email=Email,reply_blog=reply_blog,Date=datetime.today())
        cmt.save()

    return redirect('blog_temp',id=id)




#----------------------------------------Admin:-Login--------------------------------------------------
def admin_login (request):

        if request.method == "POST":
            u_name = request.POST.get('username')
            password = request.POST.get('Password')

            if not User.objects.filter(username=u_name).exists():
                messages.error(request,'Invalid Username')
                return redirect('admin_login')

            user=authenticate(username=u_name,password=password)

            if user is None:
                messages.error(request,'Invalid Password')
                return redirect('admin_login')
            else:
                 login(request,user)
                 return redirect('admin_home')
            
        return render(request,"admin_login.html")


#----------------------------------------Admin:-LogOut--------------------------------------------------
def logout_admin (request):
           
        logout(request)
        return redirect('admin_login')

#----------------------------------------Admin:-register--------------------------------------------------
@login_required(login_url='admin_login')

def admin_register(request):
    new_noti = notification.objects.all()
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        u_name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user_exists = User.objects.filter(username=u_name).exists()
        if user_exists:
            messages.error(request, 'Username is already taken')
            return redirect('admin_register')

        if not has_alpha_num_sym(password):
            messages.error(request, 'Password not alphanumeric and symbolic')
            return redirect('admin_register')
        
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('admin_register')

        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=u_name,
            email=email
        )
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created successfully!!')
        return redirect('admin_register')

    context={'new_noti':new_noti}
        
    return render(request,"admin_admin_add.html",context)



#for checking given str is sym or not
def has_alpha_num_sym(input_string):
    has_alpha = False
    has_num = False
    has_sym=False

    for char in input_string:
        if char.isalpha():
            has_alpha = True
        elif char.isdigit():
            has_num = True
        if not char.isalnum():
            has_sym=True

    return has_alpha and has_num and has_sym






#----------------------------------------Admin:-Home--------------------------------------------------
@login_required(login_url='admin_login')
def admin_home (request):

    # user_profile=request.user.userprofile

    #notification (new)
    new_noti=notification.objects.all()

    #customer msgs
    day_count=customer.objects.filter(Date=datetime.today()).count()
    total_count=customer.objects.count()

    #website visit
    day_visit=IPAddress.objects.filter(timestamp=datetime.today().date()).count()
    total_visit=IPAddress.objects.count()


    current_date = datetime.now().date()
    previous_7_days = []
    previous_7_day_view_data = []
    previous_7_day_msg_data = []


    for i in range(1, 8):
        previous_day = current_date - timedelta(days=i)
        previous_7_days.append(previous_day)

    previous_7_days.reverse()

    for j in range(len(previous_7_days)):
        
        day_data=IPAddress.objects.filter(timestamp=previous_7_days[j]).count()
        previous_7_day_view_data.append(int(day_data))

    for k in range(len(previous_7_days)):
        
        day_data=customer.objects.filter(Date=previous_7_days[k]).count()
        previous_7_day_msg_data.append(int(day_data))


    context={
            'day_count':day_count,
            'total_count':total_count,
            'day_visit':day_visit,
            'total_visit':total_visit,
            'previous_7_days':previous_7_days,
            'previous_7_day_view_data':previous_7_day_view_data,
            'previous_7_day_msg_data':previous_7_day_msg_data,
            'new_noti':new_noti,

            }
    
    return render(request,"admin_dashboard.html",context)


#----------------------------------------Admin:-team--------------------------------------------------
@login_required(login_url='admin_login')
def admin_team(request):

    #notification (new)
    new_noti=notification.objects.all()

    member=Team_Member.objects.all()
    result=None
    data=None
    
    if member:
        if request.GET.get('Search'):
            member= member.filter(Name__icontains=request.GET.get('Search'))
            data=request.GET.get('Search')[0:7]
            result=True
            
        if not member:
            data=request.GET.get('Search')[0:7]
            result=False
  
    context={'member':member,'result':result,"data":data,'new_noti':new_noti}
    return render(request,"admin_team.html",context)

#----------------------------------------Admin:-team--------------------------------------------------
@login_required(login_url='admin_login')
def add_team(request):

    if request.method == "POST":
        
        name = request.POST.get('Name')
        Qulification= request.POST.get('Qulification')
        Description = request.POST.get('Description')
        photo=request.FILES.get('Photo')

        add_team=Team_Member(Name=name,Qualification=Qulification, Description=Description,Image=photo)
        add_team.save()

        return redirect('admin_team')
    
   
#----------------------------------------Admin:-update team--------------------------------------------------    
@login_required(login_url='admin_login')
def update_team(request,id):

    #notification (new)
    new_noti=notification.objects.all()
     
    got_id=Team_Member.objects.get(id=id)


    if request.method == "POST":
        
        name = request.POST.get('Name')
        Qulification= request.POST.get('Qulification')
        Description = request.POST.get('Description')
        photo=request.FILES.get('Photo')

        got_id.Name=name
        got_id.Qualification=Qulification
        got_id.Description=Description
    
        if photo:
            got_id.Image=photo

        got_id.save()
        return redirect('/admin_team')
    
    context={'got_id':got_id,'new_noti':new_noti}
    
    return render(request, "admin_update.html",context)
    

#----------------------------------------Admin:-delete team--------------------------------------------------
@login_required(login_url='admin_login')
def delete_team(request):
     
    id=request.GET['id']
    Team_Member.objects.filter(id=id).delete()
    return redirect('/admin_team')


#----------------------------------------Admin:-Messages--------------------------------------------------
@login_required(login_url='admin_login')
def admin_msg(request):

    #notification (new)
    new_noti=notification.objects.all()

    customer_messages=customer.objects.all().order_by('-id')
    result=None
    data=None
    
    if request.GET.get('Search'):
        customer_messages= customer_messages.filter(Name__icontains=request.GET.get('Search'))
        data=request.GET.get('Search')[0:7]
        result=True
        
    if not customer_messages:
         data=request.GET.get('Search')[0:7]
         result=False

    context={'customer_messages':customer_messages,'result':result,"data":data,'new_noti':new_noti}
    return render(request,"admin_msg.html",context)


#----------------------------------------Admin:-Delete Messages--------------------------------------------------
@login_required(login_url='admin_login')
def delete_msg(request):
     
    id=request.GET['id']
    customer.objects.filter(id=id).delete()
    return redirect('/admin_msg')


@login_required(login_url='admin_login')
def admin_update(request):
    return render(request,"admin_update.html")


@login_required(login_url='admin_login')
def Appointment_section(request):

    #notification (new)
    new_noti=notification.objects.all()
     
    apt=Appointment.objects.all()[::-1]
    context={'apt':apt,'new_noti':new_noti}
    return render(request,"admin_appointment.html",context)

@login_required(login_url='admin_login')
def Create_appointment(request):#manage apt

    #notification (new)
    new_noti=notification.objects.all()

    slots=Appointment_schedule.objects.all()
    result=None
    data=None
    
    if slots:
        if request.GET.get('Search'):
            slots= slots.filter(sc_name__icontains=request.GET.get('Search'))
            data=request.GET.get('Search')[0:7]
            result=True
            
        if not slots:
            data=request.GET.get('Search')[0:7]
            result=False

    context={'slots':slots,'result':result,'data':data,'new_noti':new_noti}
    return render(request,"admin_appointment_crud.html",context)


@login_required(login_url='admin_login')
def add_appointment(request):


    if request.method == "POST":
        
        sc_name=request.POST.get('sc_name')
        start_time = request.POST.get('start_time')
        end_time= request.POST.get('end_time')

        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()



        save_slot=None
        
        if start_time > end_time:

            messages.error(request,'Please enter proper Slot')
            return redirect('/Create_appointment')
        
        if not Appointment_schedule.objects.exists():
        
            add_appointment=Appointment_schedule(sc_name=sc_name,start_time=start_time,end_time=end_time)
            add_appointment.save()
            return redirect('/Create_appointment')

        else:
            
            for i in Appointment_schedule.objects.all():

                if i.start_time > start_time and i.start_time >= end_time:

                    save_slot=True

                elif i.end_time <= start_time :

                    save_slot=True

                else:
                    save_slot=False
                    break

        if save_slot == True:

            add_appointment=Appointment_schedule(sc_name=sc_name,start_time=start_time,end_time=end_time)
            add_appointment.save()

        else:

            messages.error(request,'Your entered slot confilct with another slot')
            return redirect('/Create_appointment')


    return redirect('/Create_appointment')



@login_required(login_url='admin_login')
def update_appointment(request,id):

    #notification (new)
    new_noti=notification.objects.all()
     
    got_id=Appointment_schedule.objects.get(id=id)
    slots=Appointment_schedule.objects.all()


    if request.method == "POST":
        
        sc_name=request.POST.get('sc_name')
        start_time = request.POST.get('start_time')
        end_time= request.POST.get('end_time')


        if not start_time:
            start_time=got_id.start_time

        if not end_time:
            end_time=got_id.start_time
              
        if type(start_time) == str:
            start_time = datetime.strptime(start_time, "%H:%M").time()

        if type(end_time) == str:       
            end_time = datetime.strptime(end_time, "%H:%M").time()



        if start_time > end_time:

            messages.error(request,'Please enter proper Slot=')
            return redirect('/Create_appointment')
        

        else:
            
            for i in Appointment_schedule.objects.all():

                if got_id.id == i.id:
                    save_slot=True
                    continue
                
                if i.start_time > start_time and i.start_time >= end_time:

                    save_slot=True

                elif i.end_time <= start_time :

                    save_slot=True

                else:
                    save_slot=False
                    break

        if save_slot == True:

            got_id.sc_name=sc_name
            got_id.start_time=start_time
            got_id.end_time=end_time
        
            got_id.save()
            return redirect('/Create_appointment')  


        else:

            messages.error(request,'Your entered slot confilct with another slot=')
            return redirect('/Create_appointment')        

    
    context={'got_id':got_id,'slots':slots,'new_noti':new_noti}
    return render(request,"admin_appointment_update.html",context)



@login_required(login_url='admin_login')
def delete_appointment(request):
     
    id=request.GET['id']
    Appointment_schedule.objects.filter(id=id).delete()
    return redirect('/Create_appointment')

@login_required(login_url='admin_login')
def blog_dash(request):

    #notification (new)
    new_noti=notification.objects.all()
     

    current_date = datetime.now().date()
    previous_7_days = []
    previous_7_day_view_data = []
    all_blogs=Blog.objects.all()
    all_Blog_view_count=IPAddress_blog.objects.count()
    all_Blog_view_day_count=IPAddress_blog.objects.filter(timestamp=datetime.today().date()).count()
    top_blog=Blog.objects.order_by('-views_count')[:3]
    new_comments=comment.objects.all()[::-1][:3]


    for i in range(1, 8):
        previous_day = current_date - timedelta(days=i)
        previous_7_days.append(previous_day)

    previous_7_days.reverse()

    for j in range(len(previous_7_days)):
        
        day_data=IPAddress_blog.objects.filter(timestamp=previous_7_days[j]).count()
        previous_7_day_view_data.append(int(day_data))

    
    result=None
    data=None
    
    if request.GET.get('Search'):
        all_blogs= all_blogs.filter(Title__icontains=request.GET.get('Search'))
        data=request.GET.get('Search')[0:7]
        result=True
        
    if not all_blogs:
         data=request.GET.get('Search')[0:7]
         result=False

    context={
            'previous_7_days':previous_7_days,
            'previous_7_day_view_data':previous_7_day_view_data,
            'all_Blog_view_count':all_Blog_view_count,
            'all_Blog_view_day_count':all_Blog_view_day_count,
            'top_blog':top_blog,
            'all_blogs':all_blogs,
            'all_blogs_count':all_blogs.count(),
            'new_comments':new_comments,
            'result':result,'data':data,
            'new_noti':new_noti
            }
    
    return render(request,"admin_blog_dash.html",context)


@login_required(login_url='admin_login')
def add_blog(request):


    if request.method == "POST":
        
        Title = request.POST.get('Title')
        Para= request.POST.get('Para')
        editor= request.POST.get('editor')
        photo=request.FILES.get('Photo')

        add_Blog=Blog(Title=Title, para=Para, editor=editor,Image=photo,date_blog=datetime.today())
        add_Blog.save()

        new_blog=Blog.objects.order_by('-id').first()

        subject = 'New Article Alert:'+str(Title)
        message = '''

Dear Subscriber,

We hope this email finds you well!

We're excited to inform you about our latest article on '''+str(Title)+'''. Here are the details:

Title:'''+str(Title)+'''
URL: http://127.0.0.1:8000/blog_temp/'''+str(new_blog.id)+'''/

In this article, we delve into [brief description of the article content].

We believe this piece will be insightful and valuable to you as someone interested in Indian laws.

Feel free to click the link above to read the full article. We'd love to hear your thoughts and feedback!

Thank you for being a part of our community and staying engaged with our content.

Best regards,

-Team E-vakeel'''
        
        recipient_list = []

        for k in blog_subscribers.objects.all():

            recipient_list.append(k.Email)

        send_email(subject,message,recipient_list)

        return redirect('blog_dash')
    

@login_required(login_url='admin_login')
def delete_blog(request):
     
    id=request.GET['id']
    Blog.objects.filter(id=id).delete()
    return redirect('/blog_dash')

@login_required(login_url='admin_login')
def update_blog(request,id):

    #notification (new)
    new_noti=notification.objects.all()
     
    got_id=Blog.objects.get(id=id)

    if request.method == "POST":
        
        Title = request.POST.get('Title')
        Para= request.POST.get('para')
        editor= request.POST.get('editor')
        photo=request.FILES.get('Photo')
        print(editor)

        got_id.Title=Title
        got_id.editor=editor
        got_id.para=Para
    
        if photo:
            got_id.Image=photo

        got_id.save()
        return redirect('/blog_dash')
    
    context={'got_id':got_id,'new_noti':new_noti}
    
    return render(request, "admin_blog_update.html",context)
    

@login_required(login_url='admin_login')
def all_comment(request):
     
    #notification (new)
    new_noti=notification.objects.all()

    cmt=comment.objects.all().order_by('-id')  

    result=None
    data=None
    
    if request.GET.get('Search'):
        cmt=cmt.filter(Name__icontains=request.GET.get('Search'))
        data=request.GET.get('Search')[0:7]
        result=True
        
    if not cmt:
         data=request.GET.get('Search')[0:7]
         result=False
         
    context={'cmt':cmt,'result':result,'data':data,'new_noti':new_noti}
    return render(request,"admin_comment.html",context)

@login_required(login_url='admin_login')
def delete_comment(request):
     
    id=request.GET['id']
    comment.objects.filter(id=id).delete()
    return redirect('/all_comment')


@login_required(login_url='admin_login')
def all_subs(request):

    #notification (new)
    new_noti=notification.objects.all()

    subs = blog_subscribers.objects.all().order_by('-id')  
    result = None
    data = None

    if request.GET.get('Search'):
        subs = subs.filter(Name__icontains=request.GET.get('Search'))
        data = request.GET.get('Search')[0:7]
        result = True

    if not subs:
        data = request.GET.get('Search')[0:7]
        result = False

    context = {'subs': subs, 'result': result, 'data': data,'new_noti':new_noti}
    return render(request, "admin_subs.html", context)

@login_required(login_url='admin_login')
def delete_subs(request):
     
    id=request.GET['id']
    blog_subscribers.objects.filter(id=id).delete()
    return redirect('/all_subs')

@login_required(login_url='admin_login')

def delete_noti(request):

    id = request.GET.get('id')
    notification.objects.filter(id=id).delete()

    current_url = request.META.get('HTTP_REFERER')
    
    return redirect(current_url)

@login_required(login_url='admin_login')
def delete_noti_all(request):

    notification.objects.all().delete()
    
    # Get the current page's URL
    current_url = request.META.get('HTTP_REFERER')
    
    return redirect(current_url)



@login_required(login_url='admin_login')
def sub_admin(request):
     
    #notification (new)
    new_noti=notification.objects.all()

    adm=User.objects.all().order_by('-id')  

    result=None
    data=None
    
    if adm:
        if request.GET.get('Search'):
            adm=adm.filter(user__username__icontains=request.GET.get('Search'))
            data=request.GET.get('Search')[0:7]
            result=True
            
        if not adm:
            data=request.GET.get('Search')[0:7]
            result=False
         
    context={'adm':adm,'result':result,'data':data,'new_noti':new_noti}
    return render(request,"admin_sub_admin.html",context)

@login_required(login_url='admin_login')
def sub_admin_delete(request):

    id = request.GET.get('id')
    User.objects.filter(id=id).delete()
    
    return redirect('admin_register')
