from django.shortcuts import render, redirect

# Create your views here.
import plotly.graph_objs as go
import plotly.offline as opy
FILENAME = 'database.txt'
def home(request):
    # Initialize a dictionary to hold the state and country counts
    data = {}

    # Open the file containing the counts
    with open(FILENAME, 'r') as file:
        for line in file:
            # Split each line into state, country, and count
            location, count = line.strip().split(' : ')

            # Add the count to the data dictionary, keyed by state and country
            data[location] = int(count)

    # If the user clicked the button, update the counts and redirect back to the homepage
    if request.method == 'POST':
        # Get the state and country from the form data
        location = request.POST.get('location')

        # Increment the count for the state and country
        data[location] = data.get(location, 0) + 1

        # Open the file for writing and write the updated counts
        with open(FILENAME, 'w') as file:
            for location, count in data.items():
                file.write(f'{location} : {count}\n')

        # Redirect back to the homepage
        return redirect('home')

    # Sort the data by count in descending order
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Extract the state and country names and their corresponding counts as separate lists
    locations = []
    counts = []
    for loc, count in sorted_data:
        location.append(loc)
        counts.append(count)

    # Create a pie chart
    fig = go.Figure(data=[go.Pie(labels=locations, values=counts, hole=.3)])

    # Convert the chart to HTML
    chart = opy.plot(fig, auto_open=False, output_type='div')

    # Render the homepage template with the data and chart
    return render(request, 'home.html', {'data': sorted_data, 'chart': chart})
