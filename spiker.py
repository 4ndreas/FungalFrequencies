from datetime import datetime
import matplotlib.pyplot as plt
import numpy
import numpy as np
from statsmodels.tsa import stattools
from scipy.signal import butter, lfilter, freqz


def autocorr(x):
    result = numpy.correlate(x, x, mode='full')
    return result[result.size//2:]

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Get the filter coefficients so we can check its frequency response.
# results0 = butter_lowpass_filter(results0, cutoff, fs, order)
def getSpinkes(results0):
    spike = [0,0,0,1,0,0,0]
    spike2 = [0,0,0,0,0,1,0]
    spike3 = [0,1,0,0,0,0,0]
    # spike2 = [0,0,0.2,0.6,0.2,0,0]
    # spike = [0,0,0.5,0,0.5,0,0]
    # spike = [0,0,-0.1,0.8,-0.1,0,0]
    # spike = [0,0,-0.5,2,-0.5,0,0]
    # spike = [0,0,0.1,0.8,0.1,0,0]
    # spike = [0,0.1,0.2,0.4,0.2,0.1,0]

    lenSpike = len(spike)
    # spike = [1,1,1,2,1,1,1]
    # spike = [-2,-2,-2,-1,-2,-2,-2]
    akrSpike = stattools.acf(spike)
    correlation = []
    autocorrelation = []
    autocorrelation2 = []
    spikes = []
    filtered = []
    spikeString = ""
    stringCounter = 0
    zeroCounter = 0

    zerosDist = 20
    zeroThr = 1    

    # Filter requirements.
    order = 4
    fs = 30.0       # sample rate, Hz
    cutoff = 10  # desired cutoff frequency of the filter, Hz

    results1 = np.copy(results0)
    results0 = np.multiply(results0,-1)
    words = []

    i = 0
    while i <  len(results0)-lenSpike:
        arr = results0[i:i+lenSpike]

        corr = numpy.correlate(spike,arr, mode='same')
        # correlation.extend(corr)
        # autocorrelation.extend( arr - corr )

        s = np.clip(corr - arr,-2,0)

        corr2 = numpy.correlate(spike2,arr, mode='same')
        s = np.clip(s + np.clip(corr2 - arr,-2,0),-2,0)

        corr3 = numpy.correlate(spike3,arr, mode='same')
        s = np.clip(s + np.clip(corr3 - arr,-2,0),-2,0)

        f = np.piecewise(s, [s > -zeroThr, s <= -zeroThr], [0, 1])
        # spikes.extend(s)
        # filtered.extend(f)

        for j in range(0,len(f)):
            if f[j] == 1:
                if zeroCounter > 0:
                    zeros = ''.join(chr(ord('0')) for i in range(zeroCounter))   
                    spikeString += zeros

                spikeString += '1'
                zeroCounter = 0
                stringCounter = zerosDist
            else:
                if (stringCounter > 0):
                    stringCounter -= 1
                    zeroCounter += 1
                else:
                    if spikeString != "":
                        words.append(spikeString)
                        print(spikeString)
                        spikeString = ""
                        zeroCounter = 0
        
        i+=lenSpike
    
    # lPlot = len(correlation)
    # t = np.arange(0, lPlot, 1)
    return (words)



class spiker:
    def __init__(self):
        self.spike = [0,0,0,1,0,0,0]
        self.spike2 = [0,0,0,0,0,1,0]
        self.spike3 = [0,1,0,0,0,0,0]
        self.lenSpike = len(self.spike)

        self.spikeString = ""
        self.stringCounter = 0
        self.zeroCounter = 0

        self.zerosDist = 20
        self.zeroThr = 1    

    def getSpikes(self,results0):

        words = []

        i = 0
        results0 = np.multiply(results0,-1)
        while i <  len(results0)-self.lenSpike:
            arr = results0[i:i+self.lenSpike]
            if not None in arr[:]:
                res = self.calcSpikes(arr)
            
            if(res != ""):
                words.append(res)
            
            i+=self.lenSpike
        
        return (words)


    def calcSpikes(self,arr):

        result = ""
        thres = 2

        try:
            corr = numpy.correlate(self.spike,arr, mode='same')
            # self.correlation.extend(corr)
            # self.autocorrelation.extend( arr - corr )

            s = np.clip(corr - arr,-thres,0)

            corr2 = numpy.correlate(self.spike2,arr, mode='same')
            s = np.clip(s + np.clip(corr2 - arr,-thres,0),-thres,0)

            corr3 = numpy.correlate(self.spike3,arr, mode='same')
            s = np.clip(s + np.clip(corr3 - arr,-thres,0),-thres,0)

            f = np.piecewise(s, [s > -self.zeroThr, s <= -self.zeroThr], [0, 1])

            for j in range(0,len(f)):
                if f[j] == 1:
                    if self.zeroCounter > 0:
                        zeros = ''.join(chr(ord('0')) for i in range(self.zeroCounter))   
                        self.spikeString += zeros

                    self.spikeString += '1'
                    self.zeroCounter = 0
                    self.stringCounter = self.zerosDist
                else:
                    if (self.stringCounter > 0):
                        self.stringCounter -= 1
                        self.zeroCounter += 1
                    else:
                        if self.spikeString != "":
                            if len(self.spikeString) > 1:                            
                                result = self.spikeString
                            # print(self.spikeString)
                            self.spikeString = ""
                            self.zeroCounter = 0
        except Exception as e:
            print(e)
            print("An exception occurred in calcSpikes")                        
        
        return (result)

