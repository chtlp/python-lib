import os

'''
matplotlib fall back on 'agg' when DISPLAY is not set
** not reliable
'''
def fall_back_agg():
    import matplotlib
    print os.getenv('DISPLAY')
    if not os.getenv('DISPLAY'):
        matplotlib.use('agg')

def use_agg():
    import matplotlib
    matplotlib.use('agg')
