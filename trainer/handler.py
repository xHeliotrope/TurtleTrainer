from subprocess import Popen
from subprocess import PIPE
import retro

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

class FileHandler:
    """Used for managing backup, mp4 and data logging files
    """
    def __init__(self, file_name=game_name+game_meta, generation=0, file_number=0, video_root='recordings'):
        """set the file names
        and open up the logging file for logging

        Arguments:
          - file_name (str)
          - generation (int)
          - file_number (int)
          - video_root (str)
        """
        self.root_path = '{root}/{gen}/{number}'.format(
                root=video_root,
                gen=generation, 
                number=file_number)
        self.backup = '{root_path}/{name}.bk2'.format(
                name=file_name,
                root_path=self.root_path)
        self.video = '{root_path}/{name}.mp4'.format(
                name=file_name,
                root_path=self.root_path)
        self.file_number = file_number

    def create_video(self):
        """create video file from replay
        """
        commands = ['ve/bin/python', '-m', 'retro.scripts.playback_movie', self.backup]
        create_video_proc = Popen(commands)
        create_video_proc.wait()

    def write_turtle_stats(self, stats):
        """write the turtle stats into the directory with its backup file
        """
        with open(self.root_path + '/stats.txt', 'w+') as statfile:
            statfile.write(str(stats))

    def write_turtle_score(self, reward):
        """write the turtle score into the directory with its backup file
        """
        with open(self.root_path  + '/' + str(reward), 'w+') as rewardfile:
            rewardfile.write('boop')

    def create_video_dir(self):
        """create video file from replay
        """
        create_dir_command = 'mkdir -p ' + self.root_path
        create_video_proc = Popen(create_dir_command, shell=True, stdout=PIPE) 
        create_video_proc.wait()

    def rm_backup(self):
        """remove all backup files
        """
        try:
            rm_file_proc = Popen('rm ' + self.backup, shell=True, stdout=PIPE)
            rm_file_proc.wait()
        except FileNotFoundError:
            pass

    def rm_video(self):
        """remove all video files
        """
        try:
            rm_file_proc = Popen('rm ' + self.video, shell=True, stdout=PIPE)
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
