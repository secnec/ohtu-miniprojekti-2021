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

def search_close_matches(tips, search_term, maximum_search_results=50):
    """Returns a list of closely matching tip titles.
        Case insensitive.

    Args:
        tips (list): A list of tips.
                    Elements are assumed to be tuples.

        search_term (string): The search term to match the titles.

    Returns:
        [list]: A list of titles.
    """
    search_term_lowercase = search_term.lower()
    titles_lowercase_and_original = tip_dictionary(tips)
    close_matches_lowercase = get_close_matches(search_term_lowercase,
                             titles_lowercase_and_original.keys(),
                             n=maximum_search_results)
    matching_titles_original_case = [titles_lowercase_and_original[title] for title in close_matches_lowercase]
    return matching_titles_original_case

def tip_dictionary(tips):
    """Creates a dictionary out of a tip list
        with lowercase titles as its keys and
        the original titles as the values.

    Args:
        tips ([list]): Unchanged tip list.

    Returns:
        [dict]: Keys: lowercase titles
                values: original titles
    """
    titles = get_all_titles(tips)
    dictionary = {titles[i].lower(): titles[i] for i in range(len(tips))}
    return dictionary

