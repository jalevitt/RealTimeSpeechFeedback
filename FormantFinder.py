# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:05:03 2020

@author: jalevitt

This file contains functions for calculating VTL and for finding formants
"""

from scipy.stats import norm
import numpy as np
import scipy as sp
import scikits.talkbox
import math

def Gaussian3(x, amp1, mean1, var1, amp2, mean2, var2, amp3, mean3, var3):
    g1 = amp1 * norm.pdf((x - mean1)/var1)
    g2 = amp2 * norm.pdf((x - mean2)/var2)
    g3 = amp3 * norm.pdf((x - mean3)/var3)
    return g1 + g2 + g3

# this was a stupid idea I had early on. disregard.
# model the PSD as mixture of 3 gaussians, return the means of the gaussians
# turns out this doesnt work very well :(
def findGaussianFormantPeaks(FreqBins, PSD):
    initialGuess = [0.5, 200, 200, 0.1, 1000, 200, 0.05, 1500, 200]
    limits = (np.zeros(9),[100, 1000, 1000, 100, 2000, 1000, 100, 5000, 1000])
    popt, pcov = sp.optimize.curve_fit(Gaussian3, FreqBins, PSD, 
                                       p0 = initialGuess)#, bounds = limits)
    Formants = popt[1:8:3]
    return Formants


# Based on algorithm found at https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python
# which is in turn based on MatLab code found at https://www.mathworks.com/help/signal/ug/formant-estimation-with-lpc-coefficients.html
# which cites [1]Snell, Roy C., and Fausto Milinazzo. "Formant location from LPC analysis data." IEEE® Transactions on Speech and Audio Processing. Vol. 1, Number 2, 1993, pp. 129-134.
# and [2] Loizou, Philipos C. "COLEA: A MATLAB Software Tool for Speech Analysis."
def findFormantsLPC(Frame, fs):
    N = len(Frame)
    
    #do windowing and filtering    
    w = np.hamming(N)    
    FrameWindowed = Frame * w
    FrameFiltered = sp.signal.lfilter([1], [1., 0.63], FrameWindowed)
    
    # do LPC
    order = 2 + fs / 1000
    A, e, k = scikits.talkbox.lpc(FrameFiltered, order)
    
    # Get the roots
    rts = np.roots(A)
    rts = [r for r in rts if np.imag(r) >= 0] #select the roots with an imaginary component >=0
    
    # get angles of remaining roots
    angz = np.arctan2(np.imag(rts), np.real(rts))
    
    # convert angles to frequencies
    freqs = angz *(fs / (2 * math.pi))
    
    #calc bandwidth of roots
    bandWidth = -1/2 * (fs/(2*math.pi)) * np.log(np.abs(rts))
    
    # exclude freqs < 90Hz or bandwidth > 400Hz
    Formants = np.zeros(len(freqs))
    nFormants = 0
    for i in range(len(freqs)):
        if freqs[i] > 90 and freqs[i] < 5000 and bandWidth[i] < 500:
            Formants[nFormants] = freqs[i]
            nFormants += 1
            
    Formants = Formants[0:nFormants]
    Formants = np.sort(Formants)
        
    return Formants

# find vocal tract length from formants, based on some parameters from the Lammert paper
def getVocalTractLength(Formants, c = 34300, method = 'fd'):
    F = Formants
    lastNonZero = 0
    for i in range(len(F)):
        if F[i] != 0:
            lastNonZero = i
            
    F = F[0:lastNonZero + 1]
    if method == 'fd': #Frequency Dispersion method
        if len(F) == 1:
            L = c / (4 *  F[0])
        elif len(F) > 1:
            m = len(F)
            theta = -1 * F[0] / (2 * m - 1) + F[-1] / (2 * m - 1)
            L = c / (4 * theta)
        else:
            L = np.nan
            
    elif method == 'lammert': #Lammert Method
        beta = [0.3, 0.082, 0.124, 0.354]
        theta = 229
        for i in range(np.min([4, len(F)])):
            theta += F[i] * beta[i] / (2 * i - 1)
        L = c / (4 * theta)
    else:
        print('Invalid Vocal Tract Estimator technique')
        return False
    
    return L
    
    
