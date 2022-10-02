from typing import Dict


def sort_fun_tabs(e: Dict):
    if 'votes' in e and 'rating' in e:
        return e['votes'] * e['rating']
    else:  
        return -1


def sort_fun_hits(e: Dict):
    if 'hits' in e:
        return int(e['hits'])
    else:  
        return -1