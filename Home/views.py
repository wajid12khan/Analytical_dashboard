# dashboard/views.py
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import plotly.express as px
import pandas as pd

from .models import UploadFile
from .form import UploadFileForm

def index(request):
    form = UploadFileForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(request, 'index.html', {'form': form})



# dashboard/views.py
from django.shortcuts import render
import plotly.express as px
import pandas as pd
from .models import UploadFile

def dashboard(request):
    # Fetch the latest uploaded file
    latest_upload = UploadFile.objects.last()

    if latest_upload:
        # Construct the file path
        csv_file_path = latest_upload.uploaded_file.path

        # Read data from CSV file using pandas
        df = pd.read_csv(csv_file_path)

        # Convert the 'Date' column to datetime format if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        # Create a summary table with statistics for each numeric column
        summary_table = df.describe().to_html(classes="table table-bordered table-hover table-sm")

        # Create line charts for numeric columns over time
        line_charts = []
        for index, column in enumerate(df.select_dtypes(include='number').columns):
            if 'Date' in df.columns:
                line_fig = px.line(df, x='Date', y=column, title=f'Line Chart - {column} over Time')
            else:
                line_fig = px.line(df, x=df.index, y=column, title=f'Line Chart - {column}')
            line_charts.append((f'line_chart_{index}', line_fig.to_json()))

        # Create bar charts for categorical columns
        bar_charts = []
        for index, column in enumerate(df.select_dtypes(exclude='number').columns):
            bar_fig = px.bar(df, x=column, title=f'Bar Chart - {column}')
            bar_charts.append((f'bar_chart_{index}', bar_fig.to_json()))

        
        

        return render(request, 'dashboard.html', {
            'summary_table': summary_table,
            'line_charts': line_charts,
            'bar_charts': bar_charts,
        })

    return render(request, 'dashboard.html')
