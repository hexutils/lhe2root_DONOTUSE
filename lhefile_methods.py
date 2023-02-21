import re
import functools


class lhe_reader(object):
    def __init__(self, lhefile) -> None:
        """A class to read LHE files and perform cursory operations like 
        cutting down to size and checking equality

        Parameters
        ----------
        lhefile : str
            the .lhe file you are using

        Raises
        ------
        FileNotFoundError
            Filename should have the .lhe extension
        """
        if lhefile.split('.')[-1] != 'lhe':
            raise FileNotFoundError("LHE File Extension Required!")
        
        self.lhefile = lhefile
        self.event_selection_regex = re.compile(r'(?s)(<event>(.*?)</event>)') #regular expression to find every event
    
    @functools.cached_property #https://docs.python.org/dev/library/functools.html#functools.cached_property
    def all_events(self):
        """This function opens and collects every LHE event and puts them in a list to return
        stores the attribute as a cached property
        Returns
        -------
        list[str]
            A list of every event sequence as strings from the file (AKA everything between <event> and </event>)
        """

        with open(self.lhefile) as f:
            f = f.read()
            all_matches = re.findall(self.event_selection_regex, f)
            all_matches = [item[0] for item in all_matches]
            return all_matches
    
    @functools.cached_property
    def num_events(self):
        """Returns the number of events in the file as a cached property

        Returns
        -------
        int
            The number of events in the LHE file
        """
        return len(self.all_events)
        
    @functools.cached_property
    def non_event_portions(self):
        """This function gets everything in an LHE file that is not an event 
        (everything before the first <event> and everything after the last </event>)

        Returns
        -------
        Tuple[str, str]
            Two strings of everything before the first <event> and everything after the last </event>
        """
        with open(self.lhefile) as f:
            f = f.read()
            f_start = f[:f.find("<event>")] #everything until the first event
            f_end = f[f.rfind("</event>") + len("</event>"):] #everything after the last event
            return f_start, f_end

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, lhe_reader):
            if self.all_events == __o.all_events:
                return True
        
        return False

    def cut_down_to_size(self, n, verbose=False):
        """Cuts the number of events in an LHE file down to n events while preserving other aspects of the file

        Parameters
        ----------
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
        start_of_file, end_of_file = self.get_non_event_portions()
        
        orig_num = len(self.all_events)
        
        n = int(n)
        
        if n == orig_num:
            return start_of_file + ("\n".join(self.all_events)) + end_of_file
        elif n > orig_num:
            raise ValueError("n must be less than or equal to the number of events already in the file!")
        
        if verbose:
            print(orig_num, "events ->", n, "events")
        
        cut_down = self.all_events

        
        return start_of_file + ("\n".join(cut_down)) + end_of_file #this would ideally be placed directly into a file