# Alert class: shows an alert with buttons in canvas
class Alert:
    def __init__(self, canvas, text):
        self.text = text
        self.canvas = canvas

        # default values
        self.buttons = []
        self.visible = False
        self.buttons_canvas_label = None

    # shows the alert
    def open(self):
        # create alert text, and place it in center of canvas
        self.canvas.create_text(int(self.canvas['width']) / 2, int(self.canvas['height']) / 2, fill='black', font='Arial 14 bold', text=self.text, tags=('alert', 'alert_text',))

        # create white background for text
        r = self.canvas.create_rectangle(self.canvas.bbox('alert_text'), fill="white", tags=('alert', 'background_color'))
        # place it under the alert text
        self.canvas.tag_lower(r, 'alert_text')

        # select the first button
        if len(self.buttons) > 0:
            self.buttons[0]['selected'] = True

            # create buttons text
            self.buttons_canvas_label = self.canvas.create_text(int(self.canvas['width']) / 2,
                                                                int(self.canvas['height']) / 2 + 30, fill='black',
                                                                font='Arial 12 bold',
                                                                text=self.get_buttons_text(),
                                                                tags=('alert', 'alert_buttons',))

            # create buttons text background
            r = self.canvas.create_rectangle(self.canvas.bbox('alert_buttons'), fill="white",
                                             tags=('alert', 'background_color'))
            self.canvas.tag_lower(r, 'alert_buttons')
        self.visible = True

    # hides the alert
    def close(self):
        self.visible = False
        self.canvas.delete('alert')

    # returns True if alert is visible in canvas
    def is_visible(self):
        return self.visible

    # adds a button to the alert
    def add_button(self, text, action=False, selected=False):
        button = {'text': text, 'action': action, 'selected': selected}
        self.buttons.append(button)

    # returns the text for the buttons
    def get_buttons_text(self):
        i = 0
        buttons_text = ""
        for button in self.buttons:
            if i > 0:
                # add left margin if it's not the first
                buttons_text = buttons_text + '   '
            if button['selected']:
                # show brackets if selected
                buttons_text = buttons_text + '[' + button['text'] + ']'
            else:
                buttons_text = buttons_text + button['text']
            i = i + 1
        return buttons_text

    # renders the buttons
    def render_buttons(self):
        # set button text in canvas
        self.canvas.itemconfigure('alert_buttons', text=self.get_buttons_text())

    # keyboard listener
    def on_key_press(self, key):
        try:
            if key.char == 'a':
                self.go_left()

            if key.char == 'd':
                self.go_right()
        except Exception as e:
            # handler for special keys

            if key is key.left:
                self.go_left()

            if key is key.right:
                self.go_right()

            if key is key.enter or key is key.space:
                self.do_selected_action()

    # returns the index of the selected button
    def get_selected_button_index(self):
        i = 0
        for button in self.buttons:
            if button['selected']:
                return i
            i = i + 1

        # return -1 if no button is selected
        return -1

    # selects the next button
    def go_right(self):
        cur_selected_index = self.get_selected_button_index()
        # check if there is a right button
        if len(self.buttons) > cur_selected_index + 1:
            self.buttons[cur_selected_index]['selected'] = False
            self.buttons[cur_selected_index + 1]['selected'] = True
            self.render_buttons()

    # selects the previous button
    def go_left(self):
        cur_selected_index = self.get_selected_button_index()
        # check if there is a left button
        if cur_selected_index > 0:
            self.buttons[cur_selected_index]['selected'] = False
            self.buttons[cur_selected_index - 1]['selected'] = True
            self.render_buttons()

    # does the action of the selected button
    def do_selected_action(self):
        cur_selected_index = self.get_selected_button_index()
        button = self.buttons[cur_selected_index]
        if button['action']:
            self.close()
            button['action']()
