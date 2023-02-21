import re
import numpy as np

lhe_2_root_options = [ #these are all the possible options for lhe2root
    'vbf',
    'vbf_withdecay',
    'zh',
    'zh_withdecay',
    'zh_lep',
    'zh_lep_hawk',
    'wh_withdecay',
    'wh_lep',
    'wh',
    'ggH4l',
    'ggH4lMG',
    'use-flavor',
    'merge_photon',
    'calc_prodprob',
    'calc_decayprob',
    'CJLST',
    'MELAcalc',
    'reweight-to'
]

beautified_title = { # a dictionary to beautify your feeble and puny existence
    'costhetastard':r'$\cos(\theta*)$',
    'Phi1d':r'$\phi_1$',
    'costheta1d':r'$\cos\theta_1$',
    'costheta2d':r'$\cos\theta_2$',
    'Phid':r'$\phi$',
    'MZ1':r'$m_1$' + ' (GeV)',
    'MZ2':r'$m_2$' + ' (GeV)',
    'M4L':r'$m_{4\mu}$' + ' (GeV)' #Feel free to add to this should you desire
}

ranges = { #a dictionary of ranges to make your life easier!
    'Phid':[-np.pi, np.pi],
    'Phi1d':[-np.pi, np.pi],
    'costheta1d':[-1,1],
    'costheta2d':[-1,1],
    'costhetastard':[-1,1],
    'M4L':[6,9],
    'MZ1':[3,3.2],
    'MZ2':[3,3.2]
}

def print_msg_box(msg, indent=1, width=0, title=""):
    """Print message-box with optional title.
    Ripped from https://stackoverflow.com/questions/39969064/how-to-print-a-message-box-in-python
    Parameters
    ----------
    msg : str
        The message to use
    indent : int, optional
        indent size, by default 1
    width : int, optional
        box width, by default 0
    title : str, optional
        box title, by default ""
    """
    
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)
