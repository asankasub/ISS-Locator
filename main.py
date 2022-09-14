import requests
from datetime import datetime
import smtplib
import time
MY_LAT = -38.056309 # Your latitude
MY_LONG = 145.255615 # Your longitude
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

print(sunrise)
print(time_now)
print(sunset)


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def send_email():

    my_email = "alphwoodstock@gmail.com" 
    my_pass = "quebxagjxuawjoqm"

    if (time_now >= sunset or time_now<= sunrise) and abs(MY_LAT-iss_latitude) <= 5 and abs(MY_LONG-iss_longitude) <=5:

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, my_pass)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Look up")


on = True

while on:
    time.sleep(60)
    print("In progress")
    send_email()

