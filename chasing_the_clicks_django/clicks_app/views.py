from django.shortcuts import render, redirect

# Create your views here.
import plotly.graph_objs as go
import plotly.offline as opy
import os
import json

FILENAME = 'database.json'

def home(request):
    # Initialize a dictionary to hold the state and country counts
    data = {}

    if os.path.getsize(FILENAME) > 0:
        with open(FILENAME, 'r') as file:
            # Load the data from the file
            data = json.load(file)

    # If the user clicked the button, update the counts and redirect back to the homepage
    if request.method == 'POST':
        # Get the state and country from the form data
        location = request.POST.get('location')

        # If the location is None, set it to 'Hidden location'
        location = location or 'Hidden location'

        # Increment the count for the location
        data[location] = data.get(location, 0) + 1

        # Open the file for writing and write the updated counts
        with open(FILENAME, 'w') as file:
            # Save the data to the file
            json.dump(data, file)

        # Redirect back to the homepage
        return redirect('home')

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
    return render(request, 'home.html', {'data': sorted_data, 'chart': chart})
