from difflib import get_close_matches

def get_title(tip):
    """Returns the title of the given tip.

    Args:
        tip ([tuple]): A tip in the form of a tuple.

    Returns:
        [string]: Title of the given tip.
    """
    return tip[0]

def get_all_titles(tips):
    """Return a list of the given tips' titles.

    Args:
        tips (list): A list of tips. Elements are assumed to be tuples.

    Returns:
        [list]: A list of the given tips' titles.
    """
    titles = list(map(get_title, tips))
    return titles

def search_close_matches(tips, search_term):
    """Returns a list of closely matching tip titles.

    Args:
        tips (list): A list of tips. 
                    Elements are assumed to be tuples.
        
        search_term (string): The search term to match the titles.

    Returns:
        [list]: A list of titles.
    """
    tips_as_titles = get_all_titles(tips)
    return get_close_matches(search_term, tips_as_titles, n=50)
