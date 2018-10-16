'''
Creates a progress bar

Requires a bar_name, bar from create_bar(), total, and ticks 
'''

import sys
import math


def create_bar():
    '''
    Create a dict with strings that visually contain each
    step of the progress bar.
    '''

    bar = {}
    x = 0
    while x <= 20:
        bar[x*5] = f'|{"██"*x}{"░░"*(20-x)}|'
        x += 1

    return bar


def progress_bar(bar_name, bar, total, ticks):
    '''
    Display progress bar using bar dict
    '''

    value_per_tick = 100/total
    percent = math.floor(value_per_tick * ticks)
    remainder = percent % 5
    progress = percent - remainder

    bar_string = f'{bar_name}: {bar[progress]} {str(percent)}%'
    completed_bar_string = f'{bar_name}: {bar[100]} {str(percent)}%'

    if progress >= 100:
        print(completed_bar_string)
    else:
        sys.stdout.write(bar_string + '\r')
        sys.stdout.flush()
