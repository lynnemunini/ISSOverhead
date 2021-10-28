import requests
from datetime import datetime
import smtplib
import time

MY_LATITUDE = -1.285790
MY_LONGITUDE = 36.820030
my_email = "misslynnemunini@gmail.com"
password = ""


def overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    # iss_position = (iss_longitude, iss_latitude)

    if MY_LATITUDE-5 <= iss_latitude <= MY_LATITUDE+5 and MY_LONGITUDE-5 <= iss_longitude <= MY_LONGITUDE+5:
        return True


def is_night():
    # Used https://www.latlong.net/ to find the latitude and longitude of my location
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        # To convert the time to 24hr format
        "formatted": 0
    }

    # To know when the sun is going to rise and go down in our current location
    # Used Sunset and sunrise times API
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)

    # To get response to raise an exception if there was an error i.e 404
    response.raise_for_status()
    data = response.json()
    # Paste this https://api.sunrise-sunset.org/json?lat=-1.285790&lng=36.820030 on browser to show the data in a much
    # Nicer format
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset_hour or time_now <= sunrise_hour:
        return True


while True:
    # To run the code every 60 seconds
    time.sleep(60)
    if overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="muninilynne65@gmail.com",
                                msg=f"Subject:ISS NOTIFIER\n\nHey Lynne, The ISS is close!")





