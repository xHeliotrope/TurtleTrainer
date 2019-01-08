from subprocess import Popen
from subprocess import PIPE


class FileHandler:
    """Used for managing backup, mp4 and data logging files
    """

    def __init__(self, filename, data_file='gamedata.txt'):
        """set the file names
        and open up the logging file for logging
        """
        self.backup = filename + '.bk2'
        self.video = filename + '.mp4'
        self.f = open(data_file, 'w+')

    def create_video(self):
        """create video file from replay
        """
        create_video_command = 'python3 -m retro.scripts.playback_move ' + self.backup
        create_video_proc = Popen(create_video_command, shell=True, stdout=PIPE) 
        create_video_proc.wait()

    def rm_backup(self):
        """remove all backup files
        """
        try:
            rm_file_proc = Popen('rm *.bk2', shell=True, stdout=PIPE)
            rm_file_proc.wait()
        except FileNotFoundError:
            pass

    def rm_video(self):
        """remove all video files
        """
        try:
            rm_file_proc = Popen('rm *.mp4', shell=True, stdout=PIPE)
            rm_file_proc.communicate()
        except FileNotFoundError:
            pass

    def play_video(self):
        """play the video file
        """
        try:
            play_replay = Popen('open ' + self.video, shell=True, stdout=PIPE)
            play_replay.wait()
        except:
            play_replay = Popen('xdg-open ' + self.video, shell=True, stdout=PIPE)
            play_replay.wait()

    def log_state(self, result):
        """log the data of each action in the game

        Arguments:
          - result(str): action + reward string. looks like `[0,0,0,1,0,0,0,0,0,200]` currently
                         (key presses + last position is the reward result)
        """
        f.write(result + '\n')
        

