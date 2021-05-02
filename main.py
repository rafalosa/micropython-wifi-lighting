import picoweb
from machine import Pin
import uasyncio


pwm_pins = []
app = picoweb.WebApp(__name__)
modes = {0:"PULSE",1:"COLOR TRANS.",2:"STATIC"}
status = {0:"POWER OFF",1:"POWER ON",2:"PROGRAMMING"}
current_mode = 0
current_status = 0
power_on = False
colors = [255,255,255]


async def updateCircuit():
    global current_mode,current_status,power_on,colors

    if power_on:
        if current_mode == 0 and current_status == 1:
            uasyncio.create_task(pulseColor(colors[0]))
        elif current_mode == 1 and current_status == 1:
            uasyncio.create_task(transitionColor(colors))
        elif current_mode == 2 and current_status == 1:
            uasyncio.create_task(staticColor(colors[0]))
    else:
        pass
    return False

async def pulseColor(color):
    global current_mode,current_status
    while True:
        await uasyncio.sleep_ms(5)


        if current_mode != 0 or current_status != 1:
            break
    return False


async def transitionColor(color):
    global current_mode, current_status
    while True:
        await uasyncio.sleep_ms(5)


        if current_mode != 1 or current_status != 1:
            break
    return False


async def staticColor(color):
    global current_mode, current_status
    while True:
        await uasyncio.sleep_ms(5)
        print("static")

        if current_mode != 2 or current_status != 1:
            break
    return False


@app.route("/")
def index(req, resp):

    global power_on,current_mode,modes,current_status

    if req.method == 'POST':

        yield from req.read_form_data()

        if not power_on:

            if "power_switch" in req.form:
                power_on = not power_on
                current_status = 1
        else:

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

    else:
        req.parse_qs()

    uasyncio.create_task(updateCircuit())
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, 'website.tpl', (status[current_status],power_on))


app.run(debug=True, host="192.168.1.50")
