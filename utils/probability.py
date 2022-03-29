import numpy as np
from scipy.stats import beta

def beta_cdf_interval(interval, a, b, interval_shift):
  low = interval_shift[0]
  up = interval_shift[1]
  if up - low <= 0:
    return 0
  return beta.cdf(interval.right, a, b, loc = low, scale = up - low) -\
    beta.cdf(interval.left, a, b, loc = low, scale = up - low)

def beta_cdf_mean(interval, a, b, interval_left, interval_mean, interval_right):
  return (beta_cdf_interval(interval, a, b, interval_left) +\
    2 * beta_cdf_interval(interval, a, b, interval_mean) +\
    beta_cdf_interval(interval, a, b, interval_right)) / 4

    
def beta_cdf_mean_2d(interval, a, b, interval_mean, interval1, interval2, interval3, interval4):
  return (4*beta_cdf_interval(interval, a, b, interval_mean) +\
    beta_cdf_interval(interval, a, b, interval1) +\
    beta_cdf_interval(interval, a, b, interval2) +\
    beta_cdf_interval(interval, a, b, interval3) +\
    beta_cdf_interval(interval, a, b, interval4)) / 8


def beta_rvs_shifted(a, b, low, up):
  return beta.rvs(a, b, loc = low, scale = up - low)
  
def beta_rvs_discrete_shifted(a, b, low, up):
  return int(np.floor(beta_rvs_shifted(a,b,low,up)))




### Not used any more

def beta_cdf_diferential(event, a, b, low, up):
  epsilon = 1e-8
  return beta.cdf(event + epsilon, a, b, loc = low, scale = up - low) -\
    beta.cdf(event - epsilon, a, b, loc = low, scale = up - low)
    
def beta_cdf_discrete(event, a, b, low, up):
  return beta.cdf(event + 1, a, b, loc= low , scale= up - low) -\
      beta.cdf(event, a, b, loc= low , scale= up - low)