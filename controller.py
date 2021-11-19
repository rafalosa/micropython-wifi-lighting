from machine import Pin, PWM
import uasyncio


class LightController:

    __slots__ = {"output_pins",
                 "pwm_pins",
                 "current_mode",
                 "current_status",
                 "modes",
                 "status",
                 "power_on",
                 "colors",
                 "color",
                 "programming_flag"}
                        
    def __init__(self, output_pins):

        self.output_pins = output_pins
        self.pwm_pins = [PWM(Pin(pin, Pin.OUT), freq=500) for pin in output_pins]
        self.modes = {0: "PULSE", 1: "COLOR TRANS.", 2: "STATIC"}
        self.status = {0: "POWER OFF", 1: "POWER ON", 2: "PROGRAMMING"}
        self.power_on = False
        self.colors = [(0, 0, 0),(0, 0, 0),(0, 0, 0)]
        self.color = (0, 0, 0)
        self.programming_flag = False
        self.current_mode = 0
        self.current_status = 0

    def turn_off_outputs(self):
        
        for pin in self.pwm_pins:
            pin.duty(0)
    
    @staticmethod
    def map_values(values, max_in, max_out):
        return tuple(int(value * max_out / max_in) for value in values)
    
    @staticmethod
    def convert_colors(color_hex):
        color = color_hex.lstrip("#")
        return tuple(int(color[index:index + 2], 16) for index in range(0, 5, 2))
    
    async def update_circuit(self):
        
        if self.power_on:
            
            if self.current_mode == 0 and self.current_status == 1:
                uasyncio.create_task(self._pulse_color_loop(self.color))
                
            elif self.current_mode == 1 and self.current_status == 1:
                uasyncio.create_task(self._transition_color_loop(self.colors))
                
            elif self.current_mode == 2 and self.current_status == 1:
                uasyncio.create_task(self._static_color_loop(self.color))
        else:
            self.turn_off_outputs()
        
        return False
    
    async def _pulse_color_loop(self, color):
        
        current_time_step = 0
        time_step = 1
        max_time_step = 500
        sleep_time_ms = 5
        pulse_deadtime_ms = 500
        
        while True:
            await uasyncio.sleep_ms(sleep_time_ms)
            
            if current_time_step <= 0:
                time_step = 1
                await uasyncio.sleep_ms(pulse_deadtime_ms)
                
            elif current_time_step >= max_time_step:
                time_step = -1
            
            current_time_step += time_step
            
            for color_index, pin in enumerate(self.pwm_pins):
                pin.duty(int(color[color_index] * current_time_step / max_time_step))
                
            if self.current_mode != 0 or self.current_status != 1:
                self.turn_off_outputs()
                break
            
        return False
    
    async def _transition_color_loop(self, colors):

        pairs = ((0, 1), (1, 2), (2, 0))
        color_deltas = []
        max_time_step = 500
        sleep_time_ms = 5
        # kinda messy, find a way to beautify it.
        for pair in pairs:
            color_delta = (colors[pair[1]][0] - colors[pair[0]][0], colors[pair[1]][1] -
                           colors[pair[0]][1], colors[pair[1]][2] - colors[pair[0]][2])
            color_deltas.append(color_delta)

        while True:

            for pair, color_delta in zip(pairs, color_deltas):
                
                for time_ind in range(max_time_step):
                    
                    await uasyncio.sleep_ms(sleep_time_ms)
                    
                    for color_ind, out in enumerate(self.pwm_pins):
                        out.duty(int(colors[pair[0]][color_ind] + color_delta[color_ind] * time_ind / max_time_step))
                        
                    if self.current_mode != 1 or self.current_status != 1:
                        break

            if self.current_mode != 1 or self.current_status != 1:
                self.turn_off_outputs()
                break
            
        return False
    
    async def _static_color_loop(self, color):
        
        while True:
            await uasyncio.sleep_ms(5)

            for color_ind, out in enumerate(self.pwm_pins):
                out.duty(color[color_ind])

            if self.current_mode != 2 or self.current_status != 1:
                self.turn_off_outputs()
                break
            
        return False
    