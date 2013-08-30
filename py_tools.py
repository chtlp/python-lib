import os
import bisect
import random
import logging

def fall_back_agg():
    """
    matplotlib fall back on 'agg' when DISPLAY is not set
    ** not reliable
    """
    import matplotlib
    print os.getenv('DISPLAY')
    if not os.getenv('DISPLAY'):
        matplotlib.use('agg')

def use_agg():
    import matplotlib
    matplotlib.use('agg')

def logspace2(start, stop, num=50, endpoint=True):
    """
    logspace points between [start, stop]
    """
    from numpy import logspace, log10
    return logspace(log10(start), log10(stop), num, endpoint)

def logging_debug():
    return logging.getLogger().getEffectiveLevel() <= logging.DEBUG

def average(l):
    return sum(l) / float(len(l))

def WeightedSelectionWithReplacement(l, n):
  """Selects with replacement n random elements from a list of (item, weight) tuples."""
  cum_weight = []
  items = []
  total_weight = 0.0
  for item, weight in l:
    total_weight += weight
    cum_weight.append(total_weight)
    items.append(item)
  return [items[bisect.bisect(cum_weight, random.random()*total_weight)] for x in range(n)]
