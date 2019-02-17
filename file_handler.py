from subprocess import Popen
from subprocess import PIPE

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
        self.video_path = '{root}/{gen}'.format(root=video_root, gen=generation)
        self.backup = '{path}/{number}/{name}.bk2'.format(
                name=file_name,
                number=file_number,
                path=self.video_path)
        self.video = '{path}/{number}/{name}.mp4'.format(
                name=file_name,
                number=file_number,
                path=self.video_path)
        self.file_number = file_number

    def create_video(self):
        """create video file from replay
        """
        create_video_command = 'python3 -m retro.scripts.playback_movie ' + self.backup
        create_video_proc = Popen(create_video_command, shell=True, stdout=PIPE) 
        create_video_proc.wait()

    def write_turtle_stats(self, stats):
        """write the turtle stats into the directory with its backup file
        """
        with open(self.video_path + '/' + str(self.file_number) + '/stats.txt', 'w+') as statfile:
            statfile.write(str(stats))

    def write_turtle_score(self, reward):
        """write the turtle score into the directory with its backup file
        """
        with open(self.video_path + '/' + str(self.file_number) + '/' + str(reward), 'w+') as rewardfile:
            rewardfile.write('boop')

    def create_video_dir(self):
        """create video file from replay
        """
        create_dir_command = 'mkdir -p ' + self.video_path + str(self.file_number)
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
