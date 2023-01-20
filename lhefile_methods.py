import re
import lhe_constants


def get_all_events(lhefile):
    with open(lhefile) as f:
        f = f.read()
        all_matches = re.findall(lhe_constants.event_selection_regex, f)
        all_matches = [item[0] for item in all_matches]
        return all_matches
    
def get_non_event_portions(lhefile):
    with open(lhefile) as f:
        f = f.read()
        f_start = f[:f.find("<event>")] #everything until the first event
        f_end = f[f.rfind("</event>") + len("</event>"):] #everything after the last event
        return f_start, f_end

def cut_down_to_size(lhefile, n, verbose=False):
    all_events = get_all_events(lhefile)
    start_of_file, end_of_file = get_non_event_portions(lhefile)
    
    orig_num = len(all_events)
    
    if n == orig_num:
        return start_of_file + ("\n".join(all_events)) + end_of_file
    elif n > orig_num:
        raise ValueError("n must be less than or equal to the number of events already in the file!")
    
    if verbose:
        print(orig_num, "events ->", n, "events")
    
    all_events = all_events[:n]

    
    return start_of_file + ("\n".join(all_events)) + end_of_file