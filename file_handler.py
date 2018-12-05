from subprocess import Popen
from subprocess import PIPE


class FileHandler:

    def __init__(self, filename):
        self.backup = filename + '.bk2'
        self.video = filename + '.mp4'

    def create_video(self):
        # create video file from replay
        create_video_proc = Popen('python3 -m retro.scripts.playback_movie ' + self.backup, shell=True, stdout=PIPE) 
        create_video_proc.wait()

    def rm_backup(self):
        try:
            rm_file_proc = Popen('rm *.bk2', shell=True, stdout=PIPE)
            rm_file_proc.wait()
        except FileNotFoundError:
            pass

    def rm_video(self):
        try:
            rm_file_proc = Popen('rm *.mp4', shell=True, stdout=PIPE)
            rm_file_proc.communicate()
        except FileNotFoundError:
            pass

    def play_video(self):
        print('stuff')
        print(self.video)
        try:
            play_replay = Popen('open ' + self.video, shell=True, stdout=PIPE)
            play_replay.wait()
        except:
            play_replay = Popen('xdg-open ' + self.video, shell=True, stdout=PIPE)
            play_replay.wait()

