#%%
# tiles https://tiles.lightningmaps.org/?x=575&y=340&z=10&s=256&t=5&T=14305546
# carto https://map.lightningmaps.org/carto/10/x/y.png
# x 573-578
# y 339-34
from PIL import Image
import requests
import os
import time

from io import BytesIO
import datetime

# Define the range of x and y
x_range = range(573, 579)
y_range = range(339, 344)

#test
# x_range = range(573, 574)
# y_range = range(339, 341)

base_url = "https://map.lightningmaps.org/carto/10/{x}/{y}.png"

def get_lightning_map(base_url, x_range, y_range): #TODO speed up - slow downloading images / processing
    # Create a list to store the images
    images = []

    # Loop over the range of x and y
    for y in y_range:
        row_images = []
        for x in x_range:
            # Format the URL with the current x and y
            url = base_url.format(x=x, y=y)

            # Send a GET request to the URL
            #try 3 times
            for i in range(7):
                response = requests.get(url)
                if response.status_code == 200:
                    break
                else:
                    print(f"Error: {i}")
                    time.sleep(1)
                    pass

 # Open the image from the response
            image = Image.open(BytesIO(response.content))
# TODO moze pobrac wszystkie naraz i wtedy je polaczyc po posortowaniu, jako slownik
            # Append the image to the row_images list
            row_images.append(image)

        # Concatenate the images in the row
        row_image = Image.new('RGBA', (row_images[0].width * len(row_images), row_images[0].height), (0,0,0,0))
        for i, img in enumerate(row_images):
            row_image.paste(img, (i * row_images[0].width, 0))

        # Append the row image to the images list
        images.append(row_image)

    # Concatenate the images vertically
    final_image = Image.new('RGBA', (images[0].width, images[0].height * len(images)), (0,0,0,0))
    for i, img in enumerate(images):
        final_image.paste(img, (0, i * images[0].height))

    # Return the final image
    return final_image
    # kod pythonowy uruchamiany co kilka minut -> tworzy zdjęcie które później jest pokazywane na www

#%%
### 
### Lightnings map
###
if not os.path.exists("final_image_carto.png"):
    carto = get_lightning_map("https://map.lightningmaps.org/carto/10/{x}/{y}.png",
                  x_range, 
                  y_range)
    carto.save("final_image_carto.png")

# Get lightnings map (points)
tiles = get_lightning_map("https://tiles.lightningmaps.org/?x={x}&y={y}&z=10&s=256&t=6",
                  x_range,
                  y_range)
tiles.save("final_image_tiles.png", "PNG")

# %%
#TODO sprawdzic czy trzeba w ogole zapisywac obrazki
image1 = Image.open("final_image_carto.png") # if file exist don't initialise a function for it
image2 = Image.open("final_image_tiles.png")

image1.alpha_composite(tiles)
image1.save("final_image_combined.png")

# %%

def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

download_image("https://meteo.org.pl/img/ra.gif",
                "meteo-radar.gif")
download_image("https://meteo.org.pl/img/ra.png",
                "meteo-radar.png")
download_image("https://meteo.org.pl/img/opad.jpg",
                "meteo-opad.jpg")

#%%
# generate names of blocks for www site
# Define the time ranges and corresponding labels
time_ranges = [
    ("08:00", "11:00"),
    ("11:00", "14:00"),
    ("14:00", "17:00"),
    ("17:00", "20:00"),
    ("20:00", "23:00"),
    ("23:00", "02:00"),
    ("02:00", "05:00"),
    ("05:00", "08:00")
]

# Get the current hour in 24h format
current_hour = datetime.datetime.now().strftime("%H")

# Create a variable to store the div elements
div_elements = ""

# Loop over the time ranges
for i, (start_time, end_time) in enumerate(time_ranges):
    # Check if the current hour is within the range
    if int(start_time.split(":")[0]) <= int(current_hour) < int(end_time.split(":")[0]):
        # Generate the div id and label for the first div
        div_id = f"o{i+1}"
        current_day = datetime.datetime.now().strftime('%a')
        label = f"{current_day} {start_time}"

        # Add the first div element to the variable
        #div_elements += f'<div id="{div_id}">{label}</div>\n'
        div_elements += f'{label}\n'

        # Generate the remaining 11 divs each 3 hours later
        for j in range(1, 12):
            next_start_time = (datetime.datetime.strptime(start_time, "%H:%M") + datetime.timedelta(hours=3*j)).strftime("%H:%M")
            next_end_time = (datetime.datetime.strptime(end_time, "%H:%M") + datetime.timedelta(hours=3*j)).strftime("%H:%M")
            next_label = f"{current_day} {next_start_time}"
            if next_start_time == "23:00":
                current_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a')
            div_elements += f'{next_label}\n'
        break

# Write the div elements to a txt file
with open("meteo-opad.txt", "w") as file:
    file.write(div_elements)



# Get today's date in the format yyyymmdd
date = datetime.datetime.now().strftime("%Y%m%d")
# Get the current hour in the format HH
hour = datetime.datetime.now().strftime("%H")
# TODO add ifs
hour = "00"
url = f"https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate={date}{hour}&row=432&col=277&lang=pl"
download_image(url, "meteouw-image.png")

# %%
# Loop over the range of numbers from 0 to 99
for num in range(100):
    # Format the XX part of the URL with the current number
    url = f"https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=20240525{num:02d}&row=432&col=277&lang=pl"
#numbers are 00 06 12 18
# 06 is from 10am
# %%
