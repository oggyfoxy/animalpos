import paho.mqtt.client as mqtt
import turtle
import time
import json
import base64

wn = turtle.Screen()
wn.title("Marguerite's Positions")
marguerite = turtle.Turtle()
marguerite.penup()




def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    encoded_data = payload.get('data')
    if encoded_data:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        print(f"Received data: {decoded_data}")
        try:
            _, x, y, _ = decoded_data.split(':')
            x, y = int(x), int(y)
            marguerite.goto(x, y)
            marguerite.dot()  
        except ValueError:
            print("Could not parse the position data.")
    else:
        print("No position data found in the message.")

turtle.setup(200, 200)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "hal5")
client.on_message = on_message

client.connect("srv-lora")

client.loop_start() 
client.subscribe('#')
turtle.mainloop()

