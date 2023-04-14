from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Increment the click count
        with open('database.txt', 'a') as file:
            location = request.form['location']
            file.write(f'{location},{1}\n')

    # Get the current click count
    count = 0
    with open('database.txt', 'r') as file:
        for line in file:
            location, clicks = line.strip().split(',')
            count += int(clicks)

    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Click Counter</title>
            <!-- Add meta tag for mobile responsiveness -->
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <!-- Add Google Fonts for a more elegant font -->
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans">
            <style>
                /* Add some basic styling for the body */
                body {
                    font-family: 'Open Sans', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }

                /* Add some styling for the header */
                header {
                    background-color: #333;
                    color: #fff;
                    padding: 1rem;
                    text-align: center;
                }

                /* Add some styling for the main section */
                main {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 80vh;
                }

                /* Add some styling for the button */
                button {
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    padding: 1rem 2rem;
                    border-radius: 0.25rem;
                    cursor: pointer;
                    font-size: 1.5rem;
                    transition: all 0.2s ease-in-out;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                }

                /* Add some styling for the button on hover */
                button:hover {
                    background-color: #0056b3;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
                }

                /* Add some styling for the count display */
                #count {
                    font-size: 4rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                    color: #333;
                    text-align: center;
                }

                /* Add some styling for the footer */
                footer {
                    background-color: #333;
                    color: #fff;
                    padding: 1rem;
                    text-align: center;
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Click Counter</h1>
            </header>
            <main>
                <h2>Your Click Count:</h2>
                <h3 id="count">{}</h3>
                <button onclick="incrementCount()">Click me!</button>
                <script>
                    var count = {};

                    function incrementCount() {
                        // Get the current count
                        var countElement = document.getElementById('count');
                        var currentCount = parseInt(countElement.textContent);

                        // Increment the count
                        currentCount += 1;
                        countElement.textContent = currentCount;

                        // Send the count to the server
                        fetch('/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            body: `location=${window.location.href}`
                        });
                    }
                </script>
            </main>
            <footer>
                &copy; 2023 - Click Counter
            </footer>
        </body>
        </html>
    """.format(count)
