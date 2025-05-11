import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Create the Dash app
app = dash.Dash(__name__)

# List of places with their corresponding latitudes, longitudes, names, and images
places = [
    {"name": "Meenakshi Temple", "latitude": 9.9194, "longitude": 78.1198, "image": "Meenakshi Temple, Madurai.jpg"},
    {"name": "Konark Sun Temple", "latitude": 20.9028, "longitude": 86.0949, "image": "Konarka_Temple.jpg"},
    {"name": "RED FORT", "latitude": 28.6562, "longitude": 77.2410, "image": "Delhi_fort.jpg"},
    {"name": "Gateway of India", "latitude": 18.9220, "longitude": 72.8347, "image": "Gateway of India.jpg"},
    {"name": "Big temple", "latitude": 10.787009928616776, "longitude":  79.13769864949367, "image": "licensed-image.jpeg"},
]

# Extract latitudes, longitudes, and names for the hover functionality
latitudes = [place["latitude"] for place in places]
longitudes = [place["longitude"] for place in places]
names = [place["name"] for place in places]

# Create the scatter mapbox plot
fig = go.Figure(go.Scattermapbox(
    lat=latitudes,
    lon=longitudes,
    mode='markers',
    marker=go.scattermapbox.Marker(size=10),
    text=names,  # This will show the place name when hovering
    hoverinfo='text'
))

# Set the layout with the Mapbox token (replace 'YOUR_MAPBOX_ACCESS_TOKEN' with your Mapbox token)
fig.update_layout(
    mapbox=dict(
        accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",  # Replace with your Mapbox token
        style="open-street-map",
        zoom=4,  # Zoom level
        center=dict(lat=20.5937, lon=78.9629)  # Centered on India
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

# Layout of the Dash app
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig),
    html.Div(id='image-container', children='Click on a marker to see the image', style={'textAlign': 'center'}),
    html.Img(id='image-display', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'})
])


# Callback to update the image based on the clicked point
@app.callback(
    [Output('image-container', 'children'),
     Output('image-display', 'src')],
    [Input('map', 'clickData')]
)
def display_image(clickData):
    if clickData is None:
        return "Click on a marker to see the image", None

    # Get the clicked point's name
    clicked_name = clickData['points'][0]['text']

    # Find the corresponding image for the clicked place
    for place in places:
        if place["name"] == clicked_name:
            image_path = place["image"]
            return f"Image of {clicked_name}", f"assets/{image_path}"

    return "Image not found", None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
