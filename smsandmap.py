import math
import geocoder
import smtplib
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
SENDER_EMAIL = 
RECEIVER_EMAIL = 
PASSWORD = 

def send_email(description):
    """Send an emergency alert email with the given description."""
    subject = "Emergency Alert: Woman Requesting Help"
    body = f"A woman has requested help. Please check the details below.\n\nAI statement: {description}\n\nThank you."
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on Earth."""
    R = 6371.0  # Radius of Earth in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# Get person's location based on IP
def map():
    g = geocoder.ip('me')
    if g.latlng:
        person_lat, person_lon = g.latlng
    else:
        print("Could not determine location.")
        exit()

    print(f"Person's Location: Latitude: {person_lat}, Longitude: {person_lon}\n")

    # Police stations data
    police_stations = [
        {'name': 'Ghatkesar Police Station', 'latitude': 17.4436753, 'longitude': 78.6939807},
        {'name': 'Uppal Police Station', 'latitude': 17.4024925, 'longitude': 78.5603371},
        {'name': 'Nagole Police Station', 'latitude': 17.3781107, 'longitude': 78.5602807},
        {'name': 'L.B. Nagar Police Station', 'latitude': 17.3457176, 'longitude': 78.5522296},
        {'name': 'Medipalli Police Station', 'latitude': 17.4076477, 'longitude': 78.6006642}
    ]

    # Find the nearest police station
    min_distance = float('inf')
    nearest_station = None
    nearest_station_lat = None
    nearest_station_lon = None

    for station in police_stations:
        distance = haversine(person_lat, person_lon, station['latitude'], station['longitude'])
        print(f"Distance from {station['name']} to person: {distance:.2f} km")
        
        if distance < min_distance:
            min_distance = distance
            nearest_station = station['name']
            nearest_station_lat = station['latitude']
            nearest_station_lon = station['longitude']

    # Send email with the location and Google Maps link
    send_email(f"A woman is requesting help. You can track her location at:\nhttps://www.google.com/maps?q={person_lat},{person_lon}")

    # Open Google Maps showing the route from person to the nearest police station
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={person_lat},{person_lon}&destination={nearest_station_lat},{nearest_station_lon}"
    webbrowser.open(maps_url)

    print(f"\nThe nearest police station is: {nearest_station} with a distance of {min_distance:.2f} km.")
