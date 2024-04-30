import paho.mqtt.client as mqtt
import turtle
import time
import json
import base64

wn = turtle.Screen()
wn.title("Marguerite's Positions")
marguerite = turtle.Turtle()
marguerite.penup()

wn.bgpic('bg.gif')



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
            marguerite.write(f"({x},{y})", align="center")
        except ValueError:
            print("Could not parse the position data.")
    else:
        print("No position data found in the message.")


def draw_grid():
    axis_turtle = turtle.Turtle()
    axis_turtle.speed('fastest')
    axis_turtle.penup()

    for x in range(-200, 201, 50):
        axis_turtle.goto(x, -200)
        axis_turtle.pendown()
        axis_turtle.goto(x, 200)
        axis_turtle.penup()

    for y in range(-200, 201, 50):
        axis_turtle.goto(-200, y)
        axis_turtle.pendown()
        axis_turtle.goto(200, y)
        axis_turtle.penup()

    axis_turtle.color('black')
    axis_turtle.goto(0, -200)
    axis_turtle.pendown()
    axis_turtle.goto(0, 200)
    axis_turtle.penup()
    axis_turtle.goto(-200, 0)
    axis_turtle.pendown()
    axis_turtle.goto(200, 0)
    axis_turtle.penup()

    for number in range(-200, 201, 50):
        axis_turtle.goto(number, -5)
        axis_turtle.write(str(number), align="center")
        axis_turtle.goto(-5, number)
        axis_turtle.write(str(number), align="right")

    axis_turtle.hideturtle()

turtle.setup(200, 200)

draw_grid()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "hal5")
client.on_message = on_message

client.connect("srv-lora")

client.loop_start() 
client.subscribe('#')
turtle.mainloop()
