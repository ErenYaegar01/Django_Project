from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import Metadata, Synthesizer, CustomUser
from .forms import MetadataForm, SynthesizerForm, ExcelUploadForm
import openpyxl
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import LogoutView,  PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .utils import generate_otp, send_otp_email
from django.contrib import messages
import random
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generator:login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
        return render(request, 'generator\signup.html', {'form': form})  # Render the signup form



@login_required
def home(request):
    return render(request, 'generator/home.html')  # This is the protected page (the generator home page)


User = get_user_model()
# Login view
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        print("POST request received")
        
        # Get username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated user: {user}")
        
        if user:
            # Log in the user
            login(request, user)
            print(f"User {user.username} logged in successfully.")
            
            # Redirect to the homepage using its URL name
            return redirect('generator:home')  # Replace 'home' with the actual URL name defined in your `urls.py`
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password")
    
    # Render the login page
    return render(request, 'generator/login.html')

def home_view(request):
    return render(request, 'generator/home.html')  # Render the home page template


# Logout view
class CustomLogoutView(LogoutView):
    next_page = '/generator/login/'  # Redirect after logout (e.g., to home page)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')  # Use reverse_lazy here
    email_template_name = 'password_reset_email.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        request = self.request
        context = {
            'domain': get_current_site(request).domain if request else 'localhost:8000',
            'protocol': 'https' if request.is_secure() else 'http',
        }
        """Override to include the request context."""
        form.save(
            request=self.request,  # Pass the request here
            use_https=self.request.is_secure(),  # Determine if HTTPS should be used
            email_template_name='password_reset_email.html',
            extra_email_context=context,
        )
        return super().form_valid(form)

def custom_logout(request):
    logout(request)  # This will log out the user
    return redirect('login')  # Redirect to login page after logging out

def metadata_upload(request):
    if request.method == "POST":
        form = MetadataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('metadata_list')
    else:
        form = MetadataForm()
    return render(request, 'generator/metadata_upload.html', {'form': form})


def metadata_list(request):
    metadata = Metadata.objects.all()
    return render(request, 'generator/metadata_list.html', {'metadata': metadata})


def synthesizer_create(request):
    if request.method == "POST":
        form = SynthesizerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('synthesizer_list')
    else:
        form = SynthesizerForm()
    return render(request, 'generator/synthesizer_create.html', {'form': form})


def synthesizer_list(request):
    synthesizers = Synthesizer.objects.all()
    return render(request, 'generator/synthesizer_list.html', {'synthesizers': synthesizers})

def parse_excel(file):
    # Open the uploaded Excel file
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    data = []

    # Iterate through the rows and columns to extract data
    for row in sheet.iter_rows(values_only=True):
        data.append(row)

    return data

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel_file']
            data = parse_excel(file)

            return render(request, 'show_excel.html', {'data': data})

    else:
        form = ExcelUploadForm()

    return render(request, 'upload_excel.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        if str(entered_otp) == str(stored_otp):
            user = User.objects.get(id=user_id)
            login(request, user)
            # Clear session data
            request.session.pop('otp', None)
            request.session.pop('user_id', None)
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('verify_otp')
    return render(request, 'generator/verify_otp.html')  # Render OTP verification page

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,  # Ensure the request is passed here
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html'
            )
            return HttpResponseRedirect(reverse('generator:password_reset_done'))
    else:
        form = PasswordResetForm()

    return render(request, 'generator/password_reset_form.html', {'form': form})

def some_view(request):
    print(request.method)
    return redirect(reverse('generator:password_reset_done'))