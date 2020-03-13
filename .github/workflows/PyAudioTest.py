# -*- coding: utf-8 -*-
import pyaudio
import numpy as np


def AudioData(fs, chunkSize, Iters, Random = 0):
    if Random == 0:
        p = pyaudio.PyAudio()
        audioStream = p.open(format = pyaudio.paInt16, channels = 1, rate = fs, 
                             input = True, frames_per_buffer = chunkSize)
                        
        for i in range(Iters):
            data = np.fromstring(audioStream.read(chunkSize), dtype = np.int16)
            print(data)
            
        audioStream.stop_stream()
        audioStream.close()
        p.terminate()
    else:
        for i in range(Iters):
            data = np.random.rand(chunkSize, 1)
            print(data)
            
def getChunk(chunkSize, audioStream, Random = 0):
    if Random == 0:
        data = np.fromstring(audioStream.read(chunkSize), dtype = np.int16)
    else:
        data = np.random.rand(chunkSize, 1)
        
    return data
    
def centerClip(chunk):
    clipPercent = 0.4
    chunk = chunk - np.mean(chunk)
    mx = np.max(chunk)
    mn = np.min(chunk)
    idxA = chunk < clipPercent * mx
    idxB = chunk > clipPercent * mn
    idxClip = idxA & idxB
    chunk[idxClip] = 0
    #chunk[not idxA] = chunk[not idxA] - clipPercent * mx
    #chunk[not idxB] = chunk[not idxB] - clipPercent * mn
    return chunk

def autocorr(chunk):   
    corr = np.correlate(chunk, chunk, mode = 'full')   
    corr = corr[corr.size/2:]
    return corr
    
def getF0(acf, fs):
    minIDX = np.round(fs/200)
    F0IDX = minIDX + np.argmax(acf[minIDX:])
    return fs / F0IDX
    
