from pygame import mixer


# Background Music class: handles the background music
class BackgroundMusic:
    def __init__(self):
        # source: https://www.youtube.com/watch?v=F4agKrnnk5c
        self.music_file = './assets/audio/background_music.mp3'

        # init the pygame mixer
        mixer.init()
        mixer.music.load(self.music_file)

    # starts the music
    def start(self):
        # play music in loop
        mixer.music.play(-1)

    # stops the music
    def stop(self):
        mixer.music.fadeout(400)
