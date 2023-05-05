from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse
from django.middleware import csrf
import plotly.graph_objs as go
import plotly.offline as opy
import os
import json

FILENAME = 'database.json'
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ClickCount

@csrf_exempt
def save_location_count(request):
    if request.method == 'POST':
        geoLocation = request.POST.get('geoLocation')
        print('\n\n', geoLocation)
        geoLocation = geoLocation or 'Hidden location'
        count = request.POST.get('count')
        print(geoLocation , count)
        update_json(geoLocation,count)

def update_json(geoLocation,count):
    if os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'r') as file:
            # Load the data from the file
            data = json.load(file)

    # Increment the count for the location
    data[geoLocation] = data.get(geoLocation, 0) + int(count)
    print(f"{geoLocation} : {data[geoLocation]}")

    # Open the file for writing and write the updated counts
    with open(FILENAME, 'w') as file:
        # Save the data to the file
        json.dump(data, file)


@csrf_exempt
def get_stats(request):
    print("hello stats")
    if os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'r') as file:
            # Load the data from the file
            data = json.load(file)
            # Create a list of tuples from the data dictionary and sort it by count in descending order
            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
            print(sorted_data)
            # Create a chart using Plotly and return it as HTML
            # Extract the state and country names and their corresponding counts as separate lists
            locations = []
            counts = []
            for loc, count in sorted_data:
                locations.append(loc)
                counts.append(count)

            # Create a pie chart
            fig = go.Figure(data=[go.Pie(labels=locations, values=counts, hole=.3)])

            # Convert the chart to HTML
            chart = opy.plot(fig, auto_open=False, output_type='div')

    # Render the homepage template with the data and chart
    response =  render(request, 'stats.html', {'data': sorted_data, 'chart': chart})
    return response

@csrf_exempt
def clickCounter(request):
    # homepage
    if request.method == 'POST':
        save_location_count(request)
        return redirect(('get_stats'))
    return render(request, 'clickCounter.html')

