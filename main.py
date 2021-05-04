import picoweb
from machine import Pin, PWM
import uasyncio

pin_index = [14, 5, 4]
pwm_pins = []

for ind in pin_index:
    # pin = Pin(ind,Pin.OUT,Pin.PULL_DOWN)  # I recommend setting pins as PULL_DOWN if your hardware supports it.
    pin = Pin(ind, Pin.OUT)
    pwm_pin = PWM(pin, freq=500)
    pwm_pins.append(pwm_pin)

app = picoweb.WebApp(__name__)

modes = {0: "PULSE", 1: "COLOR TRANS.", 2: "STATIC"}
status = {0: "POWER OFF", 1: "POWER ON", 2: "PROGRAMMING"}
current_mode = 0
current_status = 0
power_on = False
colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
single_color = (0, 0, 0)
programming_flag = 0


def turnOffOutput():
    global pwm_pins
    for out in pwm_pins:
        out.duty(0)


def mapValues(values, max_init, max_conv):
    return tuple(int(value * max_conv / max_init) for value in values)


def convertColors(color_hex):
    color = color_hex.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in range(0, 5, 2))


async def updateCircuit():
    global current_mode, current_status, power_on, colors, single_color

    if power_on:
        if current_mode == 0 and current_status == 1:
            uasyncio.create_task(pulseColor(single_color))
        elif current_mode == 1 and current_status == 1:
            uasyncio.create_task(transitionColor(colors))
        elif current_mode == 2 and current_status == 1:
            uasyncio.create_task(staticColor(single_color))
    else:
        turnOffOutput()
    return False


async def pulseColor(color):
    global current_mode, current_status, pwm_pins
    time_ind = 0
    time_step = 1
    max_time = 500  # max_time*sleep_time_ms determines the pulse duration.
    sleep_time_ms = 5
    while True:
        await uasyncio.sleep_ms(sleep_time_ms)
        if time_ind <= 0:
            time_step = 1
            await uasyncio.sleep(0.5)
        elif time_ind >= max_time:
            time_step = -1

        time_ind += time_step
        for color_ind, out in enumerate(pwm_pins):
            out.duty(int(color[color_ind] * time_ind / max_time))

        if current_mode != 0 or current_status != 1:
            turnOffOutput()
            break

    return False


async def transitionColor(colors):
    global current_mode, current_status, pwm_pins
    pairs = ((0, 1), (1, 2), (2, 0))
    color_deltas = []
    max_time = 500  # max_time*sleep_time_ms determines the pulse duration.
    sleep_time_ms = 5

    for pair in pairs:
        color_delta = (colors[pair[1]][0] - colors[pair[0]][0], colors[pair[1]][1] -
                       colors[pair[0]][1], colors[pair[1]][2] - colors[pair[0]][2])
        color_deltas.append(color_delta)

    while True:

        for pair, delta in zip(pairs, color_deltas):
            for time_ind in range(max_time):
                await uasyncio.sleep_ms(sleep_time_ms)
                for color_ind, out in enumerate(pwm_pins):
                    out.duty(int(colors[pair[0]][color_ind] + delta[color_ind] * time_ind / max_time))
                if current_mode != 1 or current_status != 1:
                    break

        if current_mode != 1 or current_status != 1:
            turnOffOutput()
            break
    return False


async def staticColor(color):
    global current_mode, current_status, pwm_pins
    while True:
        await uasyncio.sleep_ms(5)

        for color_ind, out in enumerate(pwm_pins):
            out.duty(color[color_ind])

        if current_mode != 2 or current_status != 1:
            turnOffOutput()
            break
    return False


@app.route("/")
def index(req, resp):
    global power_on, current_mode, modes, current_status, programming_flag, colors, single_color

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
                single_color = mapValues(convertColors(req.form["color_picker"]), 255, 512)
                current_status = 1

        elif current_status == 2 and current_mode == 1:
            if "reprog_but" in req.form:
                programming_flag += 1
                colors[programming_flag - 1] = mapValues(convertColors(req.form["color_picker"]), 255, 512)

                if programming_flag == 3:
                    programming_flag = 0
                    current_status = 1

        elif current_status == 2 and current_mode == 2:
            if "reprog_but" in req.form:
                single_color = mapValues(convertColors(req.form["color_picker"]), 255, 512)
                current_status = 1

    else:
        req.parse_qs()

    if current_status != 2:
        turnOffOutput()
        uasyncio.create_task(updateCircuit())

    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, 'website.tpl',
                                   (status[current_status], power_on, current_mode, current_status))


app.run(debug=True, host="192.168.1.50")
