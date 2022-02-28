import numpy as np

def low_price(results:list):
    """
    This function order dicts in list by price ascending 
    and return the low expensive
    args:
        results[list] : list of dict
    Returns:
        [dict]
    """
    return sorted(results, key=lambda d: d["prix"], reverse=0)[0]


def high_rating(results:list):
    """
    This function order dicts in list by price ascending 
    and return the high rating
    args:
        results[list] : list of dict
    Returns:
        [dict]
    """

    return sorted(results, key=lambda d: float(d["note"]), reverse=1)[0]

def others_articles(results:list, hr:dict, lp:dict):
    """
        This function returns articles without
        the high rating and the le low price
        Args:
            resulst[list]: list of dict
            hr[dict]: article high rating
            lp[dict]: article low price
        Returns:
            list of dict
    """
                    
    return [dic for dic in results if dic["description"] not in [hr["description"], lp['description']] ]
