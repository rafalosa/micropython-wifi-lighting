import picoweb
from machine import Pin,PWM
import uasyncio


pin_index = [14,5,4]
pwm_pins = []

for ind in pin_index:
    pin = Pin(ind)
    pwm_pin = PWM(pin,freq=500)
    pwm_pins.append(pwm_pin)

app = picoweb.WebApp(__name__)

modes = {0:"PULSE",1:"COLOR TRANS.",2:"STATIC"}
status = {0:"POWER OFF",1:"POWER ON",2:"PROGRAMMING"}
current_mode = 0
current_status = 0
power_on = False
colors = [[500,0,0],[200,500,350],[0,0,500]]
programming_flag = 0


async def updateCircuit():
    global current_mode,current_status,power_on,colors

    if power_on:
        if current_mode == 0 and current_status == 1:
            uasyncio.create_task(pulseColor(colors[1]))
        elif current_mode == 1 and current_status == 1:
            uasyncio.create_task(transitionColor(colors))
        elif current_mode == 2 and current_status == 1:
            uasyncio.create_task(staticColor(colors[0]))
    else:
        for pin in pwm_pins:
            pin.duty(0)
    return False


async def pulseColor(color):
    global current_mode,current_status,pwm_pins
    duty = 0
    step = 0
    while True:
        await uasyncio.sleep_ms(5)
        if duty <= 0:
            step = 1
        elif duty >= 512:
            step = -1

        duty += step
        pwm_pins[0].duty(int(color[0]*duty/512))
        pwm_pins[1].duty(int(color[1]*duty/512))
        pwm_pins[2].duty(int(color[2]*duty/512))

        if current_mode != 0 or current_status != 1:
            pwm_pins[0].duty(0)
            pwm_pins[1].duty(0)
            pwm_pins[2].duty(0)
            break
    return False


async def transitionColor(color):
    global current_mode, current_status,pwm_pins

    while True:
        await uasyncio.sleep_ms(5)

        if current_mode != 1 or current_status != 1:
            pwm_pins[0].duty(0)
            break
    return False


async def staticColor(color):
    global current_mode, current_status,pwm_pins
    while True:
        await uasyncio.sleep_ms(5)

        if current_mode != 2 or current_status != 1:
            break
    return False


@app.route("/")
def index(req, resp):

    global power_on,current_mode,modes,current_status,programming_flag

    if req.method == 'POST':

        yield from req.read_form_data()

        if not power_on:

            if "power_switch" in req.form:
                power_on = not power_on
                current_status = 1

        elif current_status != 2:

            if not req.form:
                power_on = not power_on
                current_status = 0

            elif "pulse_but" in req.form:
                current_mode = 0

            elif "trans_but" in req.form:
                current_mode = 1

            elif "static_but" in req.form:
                current_mode = 2

            elif "reprog_but" in req.form and current_mode != 3:
                current_status = 2

        elif current_status == 2 and current_mode == 0:
            if "reprog_but" in req.form:
                #set color
                current_status = 1

        elif current_status == 2 and current_mode == 1:
            if "reprog_but" in req.form:
                programming_flag += 1
                #set one color each time confirm button is pressed

                if programming_flag == 3:
                    programming_flag = 0
                    current_status = 1

        elif current_status == 2 and current_mode == 2:
            if "reprog_but" in req.form:
                # set color
                current_status = 1
    else:
        req.parse_qs()

    if current_status != 2:
        uasyncio.create_task(updateCircuit())

    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, 'website.tpl', (status[current_status],power_on,current_mode,current_status))


app.run(debug=True, host="192.168.1.50")
