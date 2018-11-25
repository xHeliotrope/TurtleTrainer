#!/usr/bin/env python3
import retro
from subprocess import Popen, PIPE


if __name__ == "__main__":
    # rm TMNT video, if there is one
    try:
        tmnt_video_file = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes-1Player.Leo.Level1-000000.mp4'
        rm_file_proc = Popen('rm ' + tmnt_video_file, shell=True, stdout=PIPE)
        rm_file_proc.communicate()
    except FileNotFoundError:
        pass
    # rm TMNT replay, if there is one
    tmnt_bk_file = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes-1Player.Leo.Level1-000000.bk2'
    rm_file_proc = Popen('rm ' + tmnt_bk_file, shell=True, stdout=PIPE)
    rm_file_proc.communicate()

    env = retro.make(game='TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes', record='.')
    env.reset()
    while 1:
        sample_action = env.action_space.sample()
        while(sample_action[1] == 1):
            sample_action = env.action_space.sample()
        _obs, _rew, done, _info = env.step(sample_action)
        if done:
            break

    # create video file from replay
    create_video_proc = Popen('python3 -m retro.scripts.playback_movie ' + tmnt_bk_file, shell=True, stdout=PIPE) 
    create_video_proc.wait()

    # open up the replay
    play_replay = Popen('open ' + tmnt_video_file, shell=True, stdout=PIPE)
    play_replay.communicate()

