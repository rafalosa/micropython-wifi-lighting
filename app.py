import controller
import picoweb
import uasyncio


class PicowebAppWrapper:
    
    web_app = None
    
    def __init__(self):
        
        self.web_app = picoweb.WebApp("__main__")
        self.lighter = controller.LightController([14, 5, 4])
        self.web_app.add_url_rule("/", self.index)
        
    def run(self):
        self.web_app.run(debug=True, host="192.168.1.50")
        
    def index(self, req, resp):
        
        if req.method == 'POST':

            yield from req.read_form_data()

            if not self.lighter.power_on:

                if "power_switch" in req.form:
                    self.lighter.power_on = not self.lighter.power_on
                    self.lighter.current_status = 1

            elif self.lighter.current_status != 2:

                if not req.form:
                    self.lighter.power_on = not self.lighter.power_on
                    self.lighter.current_status = 0

                elif "pulse_but" in req.form:
                    self.lighter.current_mode = 0

                elif "trans_but" in req.form:
                    self.lighter.current_mode = 1

                elif "static_but" in req.form:
                    self.lighter.current_mode = 2

                elif "reprog_but" in req.form and self.lighter.current_mode != 3:
                    self.lighter.current_status = 2

            elif self.lighter.current_status == 2 and self.lighter.current_mode == 0:
                if "reprog_but" in req.form:
                    self.lighter.color = controller.LightController.map_values(
                        controller.LightController.convert_colors(req.form["color_picker"]), 255, 512)

                    self.lighter.current_status = 1

            elif self.lighter.current_status == 2 and self.lighter.current_mode == 1:
                if "reprog_but" in req.form:
                    self.lighter.programming_flag += 1
                    self.lighter.colors[self.lighter.programming_flag - 1] = controller.LightController.map_values(
                        controller.LightController.convert_colors(req.form["color_picker"]), 255, 512)

                    if self.lighter.programming_flag == 3:
                        self.lighter.programming_flag = 0
                        self.lighter.current_status = 1

            elif self.lighter.current_status == 2 and self.lighter.current_mode == 2:
                if "reprog_but" in req.form:
                    self.lighter.color = controller.LightController.map_values(
                        controller.LightController.convert_colors(req.form["color_picker"]), 255, 512)
                    self.lighter.current_status = 1

        else:
            req.parse_qs()

        if self.lighter.current_status != 2:
            self.lighter.turn_off_outputs()
            uasyncio.create_task(self.lighter.update_circuit())

        yield from picoweb.start_response(resp)
        yield from self.web_app.render_template(resp, 'website.tpl',
                                                (self.lighter.status[self.lighter.current_status],
                                                 self.lighter.power_on, self.lighter.current_mode,
                                                 self.lighter.current_status))
