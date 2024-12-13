from django.shortcuts import render, redirect
from .models import  Metadata, AuditLog
from .forms import MetadataForm, UserLoginForm, UploadFileForm
from django.contrib.auth import authenticate, login
import pandas as pd
from google.cloud import bigquery
from sdv.metadata import SingleTableMetadata,  MultiTableMetadata
from django.contrib import messages
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.multi_table import HMASynthesizer
import json
from django.contrib.auth import logout

def home(request):
    return render(request, 'generator/home.html')

def logout_view(request):
    # Logs out the user
    return redirect('generator:home')


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('generator:home')  # Correctly redirecting to home page.
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    
    return render(request, 'generator/login.html', {'form': form})

def generate_metadata(request):
    if request.method == 'POST':
        form = MetadataForm(request.POST)
        if form.is_valid():
            table_name = form.cleaned_data['table_name']
            data_limit = form.cleaned_data['data_limit']
            metadata_choice = form.cleaned_data['metadata_choice']

            # Query BigQuery to get the data.
            client = bigquery.Client()
            sql_query = f"SELECT * FROM `{table_name}` LIMIT {data_limit}"
            df = client.query(sql_query).to_dataframe()

            # Generate metadata based on the table structure.
            metadata = SingleTableMetadata()
            metadata.detect_from_dataframe(df)
            metadata_json = metadata.to_json()

            # Save metadata to database.
            Metadata.objects.create(table_name=table_name, metadata_json=metadata_json)

            # Log the action.
            AuditLog.objects.create(user=request.user, action=f'Metadata generated for {table_name}')

            return redirect('home')
    else:
        form = MetadataForm()

    return render(request, 'generator/generate_metadata.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # Determine the appropriate engine based on file extension
            if uploaded_file.name.endswith('.xlsx'):
                engine = 'openpyxl'
            elif uploaded_file.name.endswith('.xls'):
                engine = 'xlrd'
            else:
                return render(request, 'generator/upload.html', {
                    'form': form,
                    'error': 'Invalid file type. Please upload an Excel (.xls or .xlsx) file.'
                })

            try:
                # Read the uploaded Excel file into a DataFrame
                df = pd.read_excel(uploaded_file, engine=engine)
            except ValueError as e:
                return render(request, 'generator/upload.html', {
                    'form': form,
                    'error': f'Error reading the Excel file: {str(e)}'
                })

            num_rows = int(request.POST.get('num_rows', 10))
            metadata_dict = {}

            # Loop through each column and determine its type and additional attributes
            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    representation = "Int64" if pd.api.types.is_integer_dtype(df[column]) else "Float"
                    metadata_dict[column] = {
                        "sdtype": "numerical",
                        "computer_representation": representation
                    }
                elif pd.api.types.is_string_dtype(df[column]):
                    metadata_dict[column] = {
                        "sdtype": "categorical",
                        "regex_format": "[A-Za-z0-9]+"
                    }
                elif pd.api.types.is_datetime64_any_dtype(df[column]):
                    metadata_dict[column] = {
                        "sdtype": "datetime",
                        "computer_representation": "datetime64[ns]"
                    }
                else:
                    metadata_dict[column] = {
                        "sdtype": "unknown"
                    }

            # Create an instance of SingleTableMetadata and detect from DataFrame
            metadata = SingleTableMetadata()  # Create an instance of SingleTableMetadata
            metadata.detect_from_dataframe(df)  # Use detect_from_dataframe from SingleTableMetadata

            # Create and fit the synthesizer using the original DataFrame
            synthesizer = GaussianCopulaSynthesizer(metadata)
            synthesizer.fit(df)

            # Now sample synthetic data based on user input
            synthetic_data = synthesizer.sample(num_rows=num_rows)

            # Convert metadata dictionary to JSON for rendering or further processing
            metadata_json = json.dumps(metadata_dict, indent=4)

            # Render results page with original and synthetic data
            return render(request, 'generator/results.html', {
                'original_data': df.to_html(),
                'synthetic_data': synthetic_data.to_html(),
                'metadata_json': metadata_json,
                'success_message': 'File processed successfully!'
            })
    else:
        form = UploadFileForm()

    return render(request, 'generator/upload.html', {'form': form})

