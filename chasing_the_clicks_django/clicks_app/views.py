from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.middleware import csrf
import plotly.graph_objs as go
import plotly.offline as opy
import os
import json

FILENAME = 'database.json'

@csrf_exempt
def home(request):
    # do some processing here
    csrf_token = csrf.get_token(request)
    # Initialize a dictionary to hold the state and country counts
    data = {}

    if os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'r') as file:
            # Load the data from the file
            data = json.load(file)

    # If the user clicked the button, update the counts and redirect back to the homepage
    if request.method == 'POST':
        # Get the state and country from the form data
        location = request.POST.get('loc')
        print(f"\n\nrequest:{request}\nPOST:{request.POST}\n\n")

        # If the location is None, set it to 'Hidden location'
        location = location or 'Hidden location'

        # Increment the count for the location
        data[location] = data.get(location, 0) + 1
        print(f"{location} : {data[location]}")

        # Open the file for writing and write the updated counts
        with open(FILENAME, 'w') as file:
            # Save the data to the file
            json.dump(data, file)

        # Redirect back to the homepage
        return redirect('index.html')

    # Sort the data by count in descending order
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

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
    response =  render(request, 'index.html', {'data': sorted_data, 'chart': chart, 'csrf_token': csrf_token})
    # response.set_cookie('csrftoken', csrf_token)
    return response


from django.http import JsonResponse

def get_data(request):
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

            # Return the updated data as JSON
            return JsonResponse({'data': dict(sorted_data), 'chart': chart})

    # If the file is empty, return an empty JSON object
    return JsonResponse({})
