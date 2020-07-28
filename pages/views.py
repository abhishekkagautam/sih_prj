from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import request
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import cv2
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index_views(request):
    if request.method =="POST":
        image = request.FILES['vi']
        fs = FileSystemStorage()
        img_name=image.name
        fs.save(image.name,image)
        
            
        cap = cv2.VideoCapture(str('media/'+str(img_name)))
        frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

        out = cv2.VideoWriter("one.avi", fourcc, 5.0, (1280,720))

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        print(frame1.shape)
        while cap.isOpened():
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
            #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            image = cv2.resize(frame1, (1280,720))
            out.write(image)
            cv2.imshow("feed", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(40) == ord('q'):
                break

        cv2.destroyAllWindows()
        cap.release()
        out.release()
        return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Account created for"+user)
            return redirect('login')
    context={'form':form}
    return render(request,'reg.html',context)

def add(request):
    user=request.POST['user']
    pas=request.POST['password']
    print(user,pas)
    if user == "inco" and pas=="9876":
        return render(request,'index.html')
    else:
        return HttpResponse("<h1>qwer</h1>")
        ''''
def mark(request):
    import cv2
    img = request.FILES['']
    cap=cv2.VideoCapture(img)
    harcascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
    font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    while True:
        ret, frame = cap.read()
        if ret: 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('frame', gray)
        full_body=harcascade.detectMultiScale(frame,1.3,2)
        for (x,y,w,h) in full_body:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            cv2.putText(frame,str('Human'),(x, y+h),0,1,255)
        cv2.imshow("screen",frame)
        if cv2.waitKey(33)==ord('q'):
            break
    cv2.destroyAllWindows()'''
        