from bs4 import BeautifulSoup
import requests as req
import os
import smtplib
from email.message import EmailMessage
import time
import schedule



source = req.get('https://weather.com/en-GB/weather/today/l/51.55,-0.43?par=google&temp=c')
soup = BeautifulSoup(source.text, 'html.parser')

current_conditions = soup.find(id = 'WxuHourlyWeatherCard-main-29584a07-3742-4598-bc2a-f950a9a4d900')
current_temp = current_conditions.find(class_ = '_2v_go').text
temp_number = int(current_temp.strip('°'))

rain_chance = current_conditions.find(class_ = '_2H5Iw').text
chance_percent = int(rain_chance.strip('%'))

#extra_details = soup.find(id = 'todayDetails')
#current_wind = extra_details.find(class_ = '_1Va1P undefined').text
#wind_number = int(current_wind.strip('km/h'))


update_text = [
    'Warmer than usual.' + ' ' + str(temp_number) + '°C outside.',
    'Temp isnt too bad at the moment. Wear a jacket though.' + ' ' + str(temp_number) + '°C outside.',
    'Its cold out bro. Might wanna layer up.' + ' ' + str(temp_number) + '°C outside.',
    'Its freezing out...' + ' ' + str(temp_number) + '°C outside.',
    'Remember that snow planet on Star Wars? Yeah thats what outside is like right now.' + ' ' + str(temp_number) + '°C outside.',

    ' Also, clear skies. No need to worry about rain.' + ' ' + str(rain_chance) + ' ' + 'chance.',
    ' Also, probably isnt going to rain, but keep an eye out.' + ' ' + str(rain_chance) + ' ' + 'chance.', 
    ' Also, decent chance of rain.' + ' ' + str(rain_chance) + ' ' + 'chance.',
    ' Also, definitely gonna rain. Make sure you have your gear.' + ' ' + str(rain_chance) + ' ' + 'chance.',
]

temp_result = 'placeholder text'
rain_result = 'placeholder text'

def temp_check():
    global temp_result
    if temp_number > 15:
        temp_result = update_text[0]
    elif 10 < temp_number <= 15:
        temp_result = update_text[1]
    elif 6 < temp_number <= 10:
        temp_result = update_text[2]
    elif 1 < temp_number <= 6:
        temp_result = update_text[3]
    elif temp_number <= 1:
        temp_result = update_text[4]
    else:
        print('none')
    return


def rain_check():
    global rain_result
    if chance_percent < 10:
        rain_result = update_text[5]
    elif 10 <= chance_percent < 25:
        rain_result = update_text[6]
    elif 25 <= chance_percent < 45:
        rain_result = update_text[7]
    elif chance_percent >= 45:
        rain_result = update_text[8]
    else:
        print('none')
    return


temp_check()
rain_check()

time.sleep(2)


EMAIL_ADRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Weather alert'
msg['From'] = EMAIL_ADRESS
msg['To'] = 'kyle1443@gmail.com'
msg.set_content(temp_result + rain_result)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)

print('message sent')