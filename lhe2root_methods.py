import os
import re
import uproot
import pandas as pd
import numpy as np
import mplhep as hep
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.style.use(hep.style.ROOT)
mpl.rcParams['axes.labelsize'] = 40
mpl.rcParams['xaxis.labellocation'] = 'center'

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

def scale(counts, scaleto):
    """This function scales histograms according to their absolute area under the curve (no negatives allowed!)

    Arguments:
        counts -- A list of bin counts
        scaleto -- The absolute area to scale to

    Returns:
        The scaled histogram
    """
    counts = counts.astype(float)
    signs = np.sign(counts) #makes sure to preserve sign
    counts = np.abs(counts)
    
    return signs*counts*scaleto/np.sum(counts)

def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title.
    Ripped from https://stackoverflow.com/questions/39969064/how-to-print-a-message-box-in-python
    Arguments:
        msg -- The message to use

    Keyword Arguments:
        indent -- indent size (default: {1})
        width -- box width (default: {None})
        title -- box title (default: {None})
        
    Returns:
        None
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



def get_cross_section_from_LHE_file(LHE_file_path):
    """Gets the cross section and its uncertainty from a given LHE file using regular expressions

    Arguments:
        LHE_file_path -- The file path for the LHE file

    Returns:
        A tuple of strings containing the cross section and its uncertainty
    """
    
    cross_section = uncertainty = ""
    
    with open(LHE_file_path) as getting_cross_section:
        head = getting_cross_section.read()
        
        #This regex was made by the very very helpful https://pythex.org/ (shoutout professor Upsorn Praphamontripong)
        cross_finder = re.compile(r'<init>\n.+\n.+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})(\d|\s)+</init>')
        cross_section_match = re.search(cross_finder,head)
        
        cross_section = cross_section_match.group(1)
        
        uncertainty = cross_section_match.group(3)
        
    return cross_section, uncertainty #returns the cross section and its uncertainty        

def check_for_MELA():
    """A simple function that checks whether or not you have the environment variables for MELA set up within your terminal

    Returns:
        A boolean as to whether or not MELA is properly set up
    """
    if "LD_LIBRARY_PATH" not in os.environ: #this library path is set up by the MELA setup script
        print("MELA environment variables have not been set up correctly")
        if 'HexUtils' in os.getcwd():
            print("Run './install.sh' in the directory above HexUtils to set these up!")
        else:
            print("Run './setup.sh' in the MELA directory to set these up!")
            
        return False
    
    return True


def recursively_convert(current_directory, argument, clean=False, verbose=False, exceptions=set(), write=""):
    """This function will recurse through every directory and subdirectory in the place you call it, 
    and attempt to convert those files to ROOT files using lhe2root

    Arguments:
        current_directory -- The directory to start recursing downwards from
        argument -- the lhe2root argument to use (see lhe_2_root_options at the top of the file)

    Keyword Arguments:
        clean -- If True, this function will wipe any old conversion and re-convert the files (default: {False})
        verbose -- If true, the function will be verbose (default: {False})
        exceptions -- Any absolute path with this string in it will be ignored(default: {set()})
            NOTE: This is the case for any string in the path! folders of path <exception>/<other folder> will be ignored
            The same goes for folders where a substring of the folder matches the name in the exception - useful for catching multiple folders!
            Name your folders carefully!
        write -- If a string, this will be the file that you will write the cross sections to. The file will be comma-separated
            
    Returns:
        Returns a dictionary with the cross section/uncertainty pairs for every file
    """
    
    cross_sections = {}
    
    for candidate in os.listdir(current_directory):
        # print(candidate)
        candidate = os.fsdecode(candidate)
        
        candidate_filename = candidate[:candidate.rfind('.')]
                
        candidate = current_directory + '/' + candidate
        # print(candidate)
        
        is_exempt = False
        for exemption in exceptions:
            if exemption in candidate:
                is_exempt = True
        
        
        if (os.path.isdir(candidate)) and (not is_exempt): #convert all the LHE files in every directory below you
            one_folder_below = recursively_convert(candidate, argument, clean, verbose, exceptions)
            cross_sections.update(one_folder_below)
        
        if candidate.split('.')[-1] != 'lhe':
            if clean and candidate.split['.'][-1] == '.root':
                print_msg_box("Removing " + candidate, title="Cleaning directory " + current_directory)
                os.remove(candidate)
                
            continue
        
        else:
            output_filename = 'LHE_' + candidate_filename + '.root'
            
            running_str = "python lhe2root.py --" + argument + " " + current_directory + '/' + output_filename + ' '
            running_str += candidate
            
            if not verbose:
                running_str += ' > /dev/null 2>&1'
            
            cross_section, uncertainty = get_cross_section_from_LHE_file(candidate) #these are currently strings!
            
            cross_sections[current_directory + '/' + output_filename] = (cross_section, uncertainty)
            
            titlestr = "Generating ROOT file for ./" + os.path.relpath(candidate)
            
            print_msg_box("Input name: " + candidate.split('/')[-1] + #This is the big message box seen per LHE file found
                "\nOutput name: " + output_filename + 
                "\nArgument: " + argument + 
                "\n\u03C3: " + cross_section + " \u00b1 " + uncertainty,
                title=titlestr, width=len(titlestr))
            
            os.system(running_str)
    
    if write:
        with open(write, "w+") as f:
            f.write("Filename, Cross Section, Uncertainty\n")
            for fname, (crosssection, uncertainty) in cross_sections.items():
                f.write(fname + ', ' + crosssection + ', ' + uncertainty + '\n')
                
    return cross_sections



def plot_one_quantity(filenames, attribute, xrange, nbins=100, labels=[], norm=False, title=""):
    """This function plots one quantity of your choice from a ROOT file!

    Arguments:
        filenames -- The ROOT files you are plotting from
        attribute -- The TBranches you are plotting (the files should have the same names for branches)
        xrange -- The range for your x axis for this attribute

    Keyword Arguments:
        nbins -- The number of bins. This can either be a number or a list (default: {100})
        labels -- The labels for each file plotted (default: {[]})
        norm -- Whether to normalize the plotting areas to 1 for easier comparison (default: {False})
        title -- An extra "title" on the x label that is concatenated (default: {""})

    Raises:
        ValueError: If your list of labels and list of filenames are not the same length
        ValueError: If you choose a column that is undefined

    Returns:
        A dictionary of NumPy style histogram tuple of counts and bins with the filename as the key
    """
    if labels and len(labels) != len(filenames):
        raise ValueError("labels and files should be the same length!")
    
    histograms = {}
    
    for n, file in enumerate(filenames):
        with uproot.open(file) as f:
            keys = f.keys()
            f = f[keys[0]].arrays(library='pd')
            
            try:
                value = f[attribute]
            except:
                raise ValueError("You can only choose from these attributes:\n" + str(list(f.columns)))
            
            hist_counts, hist_bins = np.histogram(value, range=xrange, bins=nbins)
            
            histograms[file] = (hist_counts, hist_bins)
            
            if norm:
                hist_counts = scale(hist_counts, 1)
                
            if labels:
                hep.histplot(hist_counts, hist_bins, lw=2, label=labels[n])
            else:
                hep.histplot(hist_counts, hist_bins, lw=2)
                
            plt.xlim(xrange)
            
            if attribute in beautified_title:
                plt.xlabel(beautified_title[attribute] + title, horizontalalignment='center', fontsize=30)
            else:
                plt.xlabel(attribute + title, horizontalalignment='center', fontsize=30)
                
    if labels:
        plt.legend()
        
    plt.tight_layout()
    plt.show()
    
    return histograms


def plot_interference(mixed_file, pure1, pure2, pure1Name, pure2Name, attribute, cross_sections, nbins=100, title=""):
    """Plots the interference between two samples given a file containing a mixture of the two, and two "pure" samples

    Arguments:
        mixed_file -- The file containing a simulation of pure1 and pure2 together
        pure1 -- Just one of the two items (no mixing)
        pure2 -- Just the other of the two items (no mixing)
        pure1Name -- The name for what this sample is called
        pure2Name -- The name for what this sample is called
        attribute -- The thing you are plotting (i.e. M4L, phi, etc.)
        cross_sections -- A dictionary containing the cross sections of each file in the following format: 
            {filename: cross section}

    Keyword Arguments:
        nbins -- The number of bins for your plot. This can either be an integer or a list of bins (default: {100})
        title -- An extra "title" on the x label that is concatenated (default: {""})
        

    Returns:
        The interference portion between the three plots
    """
    
    mixed_file = os.path.abspath(mixed_file)
    pure1 = os.path.abspath(pure1)
    pure2 = os.path.abspath(pure2)
    
    interf_sample = BW1_sample = BW2_sample = pd.DataFrame()
    
    with uproot.open(mixed_file) as interf: #Opening all of these in the same statement might cause memory issues. So here we are!
        interf_sample = interf[interf.keys()[0]].arrays(library='pd')
        
    if attribute not in interf_sample.columns:
        return
        
    with uproot.open(pure1) as rawBW1:
        BW1_sample = rawBW1[rawBW1.keys()[0]].arrays(library='pd')
        
    with uproot.open(pure2) as rawBW2:
        BW2_sample = rawBW2[rawBW2.keys()[0]].arrays(library='pd')
        
    
    interf_hist, bins = np.histogram(interf_sample[attribute], range=ranges[attribute], bins=nbins)
    BW1_hist, _ = np.histogram(BW1_sample[attribute], range=ranges[attribute], bins=bins)
    BW2_hist, _ = np.histogram(BW2_sample[attribute], range=ranges[attribute], bins=bins)
    
    # print('%E' % CrossSections[pure1][0], '%E' % CrossSections[pure2][0], '%E' % np.sqrt(CrossSections[pure1][0]*CrossSections[pure2][0])
    #     , '%E' % CrossSections[mixed_file][0])
    
    interf_hist = scale(interf_hist, cross_sections[mixed_file])
    BW1_hist = scale(BW1_hist, cross_sections[pure1])
    BW2_hist = scale(BW2_hist, cross_sections[pure2])
    
    interf_actual = interf_hist - BW1_hist - BW2_hist
    
    plt.figure()
    plt.gca().axhline(lw=3, linestyle='--', color='black', zorder=0)
    
    hep.histplot(BW1_hist, bins, label=pure1Name, lw=2)
    hep.histplot(BW2_hist, bins, label=pure2Name, lw=2)
    hep.histplot(interf_hist, bins, label=pure1Name + '/' + pure2Name, lw=2)
    # print(interf_hist)
    
    hep.histplot(interf_actual, bins, label=pure1Name + '/' + pure2Name + ' Interference', lw=2)
    
    plt.xlabel(beautified_title[attribute] + " " + title, horizontalalignment='center', fontsize=20)
    plt.xlim(ranges[attribute])
    plt.legend()
    plt.tight_layout()
    
    plt.show()
    
    return interf_actual, bins