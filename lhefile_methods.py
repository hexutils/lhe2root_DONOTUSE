import re
import lhe_constants


def get_all_events(lhefile):
    """This function opens and collects every LHE event and puts them in a list to return

    Parameters
    ----------
    lhefile : str
        The LHE file you are working with

    Returns
    -------
    list[str]
        A list of every event sequence as strings from the file (AKA everything between <event> and </event>)
    """

    with open(lhefile) as f:
        f = f.read()
        all_matches = re.findall(lhe_constants.event_selection_regex, f)
        all_matches = [item[0] for item in all_matches]
        return all_matches
    
def get_non_event_portions(lhefile):
    """This function gets everything in an LHE file that is not an event 
    (everything before the first <event> and everything after the last </event>)

    Parameters
    ----------
    lhefile : str
        The LHE file you are working with

    Returns
    -------
    Tuple[str, str]
        Two strings of everything before the first <event> and everything after the last </event>
    """
    with open(lhefile) as f:
        f = f.read()
        f_start = f[:f.find("<event>")] #everything until the first event
        f_end = f[f.rfind("</event>") + len("</event>"):] #everything after the last event
        return f_start, f_end

def cut_down_to_size(lhefile, n, verbose=False):
    """Cuts the number of events in an LHE file down to n events while preserving other aspects of the file

    Parameters
    ----------
    lhefile : str
        The LHE file you want to cut down to size
    n : int
        The number of events you want to keep
    verbose : bool, optional
        Whether you want the function to be verbose, by default False

    Returns
    -------
    str
        A string that should be passed to a file of the LHE file

    Raises
    ------
    ValueError
        n must be <= the number of events in the file
    """
    all_events = get_all_events(lhefile)
    start_of_file, end_of_file = get_non_event_portions(lhefile)
    
    orig_num = len(all_events)
    
    n = int(n)
    
    if n == orig_num:
        return start_of_file + ("\n".join(all_events)) + end_of_file
    elif n > orig_num:
        raise ValueError("n must be less than or equal to the number of events already in the file!")
    
    if verbose:
        print(orig_num, "events ->", n, "events")
    
    all_events = all_events[:n]

    
    return start_of_file + ("\n".join(all_events)) + end_of_file #this would ideally be placed directly into a file