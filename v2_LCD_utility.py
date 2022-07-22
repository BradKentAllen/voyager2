#!/usr/bin/env python
# -*- coding: utf-8 -*-
# UI.py

''' General UI mechanic for RPi_voyager

LCD manager abstracts all LCD devices
Threads in gpiozero cause collissions in LCD
thread_manager assures LCD commands are executed one at a time

main_LCD is managed as class variable
second LCD can be created by creating a second LCD_manager
or, second LCD object must be managed in parent object
'''

import my_RPi_config as config

if config.LCD_TYPE == None:
    pass
elif config.LCD_TYPE[:3] == 'I2C':
    # import I2C LCD
    from .displays.LCD_basic import LCD as LCD_device
else:
    # XXXX - is this an error?
    pass

from .resources import custom_char_dict



class HardwareError(Exception):
    pass

class LCD_manager:
    def __init__(self):
        '''LCD_manager abstracts LCD calls and manages threads.
        LCD manager is required to maintain coherent threads
        When initiated, creates a main_lcd which is used as default LCD.
        Additional lcd objects can be created separately and fed into methods.
        '''
        if config.LCD_TYPE != None:
            self.restart_LCD()

    def create_myLCD(self):
        ''' Create and return an LCD object
        This method returns lcd object so multiple objects can be 
        created.  Even though the class has a default object.
        '''
        if config.LCD_TYPE is None:
            return None

        if config.LCD_TYPE == 'I2C/16x2':
            #### any commands here must directly control the LCD
            try:
                this_LCD = LCD_device('use config')
            except OSError:
                raise HardwareError('no LCD detectd')
            # turn backlight on (1 indicates ON)
            this_LCD.backlight(1)
            return this_LCD

        elif config.LCD_TYPE == 'I2C/20x4':
            #### any commands here must directly control the LCD
            try:
                this_LCD = LCD_device('use config')
            except OSError:
                raise HardwareError('no LCD detectd')
            # turn backlight on (1 indicates ON)
            this_LCD.backlight(1)
            return this_LCD
        elif config.LCD_TYPE == 'wired/16x2':
            print('UI.py no LCD driver set up')
            pass

    
    def restart_LCD(self, this_lcd=None):
        '''restart function for occasional redo
        '''
        if this_lcd is None:
            # load default main lcd
            self.main_lcd = self.create_myLCD()
            self.load_custom_chars(self.main_lcd)
        else:
            # load a secondary lcd provided
            this_lcd = self.create_myLCD()
            self.load_custom_chars(this_lcd)
            return this_lcd
 

    def display_clear(self, this_lcd=None):
        if this_lcd is None:
            this_lcd = self.main_lcd
        this_lcd.clear()

    def display_multi_line(self, message_list, this_lcd=None):
        '''allows sending a full display in one command.
        Format:
        message_list = [
        ('line one message', justification),
        ('line two message', justification)
        ('line three message', justification)
        ('line four message', justification)
        ]
        '''
        print('\n\n#### display multi line ####')
        print(f'\n{message_list}')
        for count, message_tuple in enumerate(message_list):
            # lines are numbered from 1
            line = count + 1
            
            # check for Python converting tuple to just string
            # takes care of this format: [('message'), ('message2')]
            if type(message_tuple) == str:
                message_tuple = (message_tuple,)
            if len(message_tuple) < 1:
                pass
            elif len(message_tuple) == 1:
                # default case is left justified at 0
                if this_lcd == None:
                    self.display_line(message_tuple[0], line, 0)
                else:
                    self.display_line(message_tuple[0], line, 0, 'left', this_lcd)
            elif len(message_tuple) == 2:
                # determine index for justification based on display size
                if message_list[1] == 'left':
                    index = 0
                elif message_list[1] == 'right':
                    index = int(config.LCD_TYPE[4:6])
                elif message_list[1] == 'center':
                    index = int(config.LCD_TYPE[4:6]) / 2
                else:
                    index = 0

                # display line
                if this_lcd == None:
                    self.display_line(message_tuple[0], line, index, message_tuple[1])
                else:
                    self.display_line(message_tuple[0], line, index, message_tuple[1], this_lcd)

            else:
                # something is wrong
                pass


    def display_line(self, message, line, index, justification='left', this_lcd=None):
        '''aligns text around an indexed location
        index: location for justification (e.g. 10 is center of display)
        justification: 'left', 'center', or 'right'
        '''
        if this_lcd is None:
            this_lcd = self.main_lcd

        length = int(len(message))
        if justification == 'center':
            location = index - (length / 2)
        elif justification == 'right':
            location = (index - length) + 1
        else:
            location = index

        this_lcd.write_string(message, line, int(location))

    def display_char(self, char, line, pos, this_lcd=None):
        '''places cursor then character
        '''
        if this_lcd is None:
            this_lcd = self.main_lcd
        # position cursor
        this_lcd.write_string('', line , pos)
        this_lcd.write_char(char) 


    def backlight_ON(self, this_lcd=None):
        if this_lcd is None:
            this_lcd = self.main_lcd
        this_lcd.backlight(1)  

 
    def backlight_OFF(self, this_lcd=None):
        if this_lcd is None:
            this_lcd = self.main_lcd
        this_lcd.backlight(0)

    def display_all_lines(self, line1, line2=None, line3=None, line4=None):
        '''General utitility for writing to all lines in display
        '''
        if type(line1) == str and line1 is not None:
            self.display_line(line1, 1, 0, 'left')

        if type(line2) == str and line2 is not None:
            self.display_line(line2, 2, 0, 'left')

        if type(line3) == str and line3 is not None:
            self.display_line(line3, 3, 0, 'left')

        if type(line4) == str and line4 is not None:
            self.display_line(line4, 4, 0, 'left')


    # add custom characters (0 - 7)
    def load_custom_chars(self, this_lcd=None):
        ''' creates custom characters
        IMPORTANT: ONLY CALL FROM METHOD WITH thread_manager
        '''
        if this_lcd is None:
            this_lcd = self.main_lcd

        #### create fontdata list of chars.  Each char has  line
        # make sure config.custom_chars is sorted by key
        # chars are input as list that must be in number order
        custom_chars = dict(sorted(config.custom_chars.items(), key=lambda item: item[1]))

        # create custom_characters dictionary
        font_data = []
        for key, value in custom_chars.items():
            try:
                font_data.append(custom_char_dict[key])
            except KeyError:
                # passes if a char is called that is not in resources.py
                pass

        #### write into lcd
        this_lcd.lcd_write(0x40);
        for char in font_data:
            for this_byte in char:
                this_lcd.write_char(this_byte)





