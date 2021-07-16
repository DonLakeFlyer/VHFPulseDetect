/* -*- c++ -*- */
/*
 * Copyright 2021 gr-VHFPulseDetect2 author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "pulse_detect_ff_impl.h"

namespace gr {
  namespace VHFPulseDetect2 {

pulse_detect_ff::sptr pulse_detect_ff::make(float threshold, float pulseDuration, int sampleRate)
{
    return gnuradio::get_initial_sptr (new pulse_detect_ff_impl(threshold, pulseDuration, sampleRate));
}


pulse_detect_ff_impl::~pulse_detect_ff_impl()
{

}

#if 0
    # https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/22640362#22640362

    We sort of follow this algorithm

    # Let y be a vector of timeseries data of at least length lag+2
    # Let mean() be a function that calculates the mean
    # Let std() be a function that calculates the standard deviaton
    # Let absolute() be the absolute value function

    # Settings (the ones below are examples: choose what is best for your data)
    set lag to 5;          # lag 5 for the smoothing functions
    set threshold to 3.5;  # 3.5 standard deviations for signal
    set influence to 0.5;  # between 0 and 1, where 1 is normal influence, 0.5 is half

    # Initialise variables
    set signals to vector 0,...,0 of length of y;   # Initialise signal results
    set filteredY to y(1),...,y(lag)                # Initialise filtered series
    set avgFilter to null;                          # Initialise average filter
    set stdFilter to null;                          # Initialise std. filter
    set avgFilter(lag) to mean(y(1),...,y(lag));    # Initialise first value
    set stdFilter(lag) to std(y(1),...,y(lag));     # Initialise first value

    for i=lag+1,...,t do
      if absolute(y(i) - avgFilter(i-1)) > threshold*stdFilter(i-1) then
        if y(i) > avgFilter(i-1) then
          set signals(i) to +1;                     # Positive signal
        else
          set signals(i) to -1;                     # Negative signal
        end
        # Make influence lower
        set filteredY(i) to influence*y(i) + (1-influence)*filteredY(i-1);
      else
        set signals(i) to 0;                        # No signal
        set filteredY(i) to y(i);
      end
      # Adjust the filters
      set avgFilter(i) to mean(filteredY(i-lag),...,filteredY(i));
      set stdFilter(i) to std(filteredY(i-lag),...,filteredY(i));
    end
#endif

pulse_detect_ff_impl::pulse_detect_ff_impl(float threshold, float pulseDuration, int sampleRate)
    : gr::sync_block        ("pulse_detect_ff", gr::io_signature::make(1, 1, sizeof(float)), gr::io_signature::make(6, 6, sizeof(float)))
    , _sampleRate           (sampleRate)
    , _pulseDuration        (pulseDuration)
    , _minSamplesForPulse   (_sampleRate * _pulseDuration / 2.0f)
    , _threshold            (threshold)
{
    _cLag                   = 10;
    _cMovingWindow          = _sampleRate * _pulseDuration * 16;
    _rgMovingAvg            = (double*)calloc(_cMovingWindow, sizeof(double));
    _rgMovingStdDev         = (double*)calloc(_cMovingWindow, sizeof(double));
    _rgMovingAvgPart        = (double*)calloc(_cMovingWindow, sizeof(double));
    _rgMovingVariancePart   = (double*)calloc(_cMovingWindow, sizeof(double));
}


int pulse_detect_ff_impl::work(int noutput_items, gr_vector_const_void_star &input_items, gr_vector_void_star &output_items)
{
    const float *in = (const float *) input_items[0];

    float *rgOutPulseDetect     = (float *) output_items[0];
    float *rgOutPulseValue      = (float *) output_items[1];
    float *rgOutMovingAvg       = (float *) output_items[2];
    float *rgOutMovingVar       = (float *) output_items[3];
    float *rgOutMovingStdDev    = (float *) output_items[4];
    float *rgOutThreshold       = (float *) output_items[5];

    for (int i=0; i<noutput_items; i++) {
        rgOutPulseDetect[i]     = 0; // no pulse detected
        rgOutPulseValue[i]      = 0;
        rgOutMovingAvg[i]       = 0;
        rgOutMovingVar[i]       = 0;
        rgOutMovingStdDev[i]    = 0;
        rgOutThreshold[i]       = 0;

        _sampleCount++;

        double pulseValue = in[i];
        if (std::isnan(pulseValue)) {
            continue;
        }

        double curSampleSeconds = _sampleCount / _sampleRate; 

        int curLagIndex = _curMovingIndex - _cLag;
        if (curLagIndex < 0) {
            curLagIndex += _cMovingWindow;
        }
        double laggingAvg       = _rgMovingAvg[curLagIndex];
        double laggingStdDev    = _rgMovingStdDev[curLagIndex];

        if (_trackingPossiblePulse) {
            if (pulseValue - laggingAvg < _threshold * laggingStdDev) {
                if (_pulseSampleCount > _minSamplesForPulse) {
                    printf("Trailing edge pulseMax(%f) pulseValue(%f) pulseSampleCount(%d) pulseSampleCountDelta(%d)\n", _pulseMax, pulseValue, _pulseSampleCount, _sampleCount - _lastPulseSampleCount);
                    rgOutPulseDetect[i] = _pulseMax;
                    _lastPulseSeconds = curSampleSeconds;
                    _lastPulseSampleCount = _sampleCount;
                } else {
                    //printf("Short pulseValue(%f) pulseMax(%f) pulseSampleCount(%d)\n", pulseValue, _pulseMax, _pulseSampleCount);
                }
                _trackingPossiblePulse = false;
                _pulseMax = 0;
                _pulseSampleCount = 0;
            } else {
                if (pulseValue > _pulseMax) {
                    _pulseMax = pulseValue;
                }
                _pulseSampleCount++;
            }
        } else {
            if (pulseValue - laggingAvg > _threshold * laggingStdDev) {
                //printf("Leading edge pulseValue(%f)\n", pulseValue);
                _trackingPossiblePulse =  true;
                _pulseMax = pulseValue;
                _pulseSampleCount = 1;
            }
            }

        // Update moving average
        double movingAvgPart = pulseValue / static_cast<double>(_cMovingWindow);
        _movingAvg -= _rgMovingAvgPart[_curMovingIndex];
        _movingAvg += movingAvgPart;
        _rgMovingAvgPart[_curMovingIndex] = movingAvgPart;
        _rgMovingAvg[_curMovingIndex] = _movingAvg;

        // Update moving variance
        double movingVariancePart = pow(pulseValue -_rgMovingAvg[_curMovingIndex], 2);
        _movingVariance -= _rgMovingVariancePart[_curMovingIndex];
        _movingVariance += movingVariancePart;
        _rgMovingVariancePart[_curMovingIndex] = movingVariancePart;

        // Update moving StdDev
        double movingStdDev = sqrt(_movingVariance / static_cast<double>(_cMovingWindow));
        _rgMovingStdDev[_curMovingIndex] = movingStdDev;

        // Update moving index
        if (_curMovingIndex == _cMovingWindow - 1) {
            _curMovingIndex = 0;
        } else {
            _curMovingIndex++;  
        }

        rgOutPulseValue[i]      = pulseValue;
        rgOutMovingAvg[i]       = _movingAvg;
        rgOutMovingVar[i]       = _movingVariance / static_cast<double>(_cMovingWindow);
        rgOutMovingStdDev[i]    = movingStdDev;
        rgOutThreshold[i]       = _movingAvg + (_threshold * movingStdDev);

#if 0
        printf("%f %f %f %f %f\n",
            rgOutPulseValue[i],
            rgOutMovingAvg[i],
            rgOutMovingVar[i],
            rgOutMovingStdDev[i],
            rgOutThreshold[i]);
#endif

        if (curSampleSeconds - _lastPulseSeconds > _noPulseTimeSecs) {
            _lastPulseSeconds = curSampleSeconds; 
            _trackingPossiblePulse = false; 
            _pulseSampleCount = 0; 
            _pulseMax = 0; 
            printf("No pulse for %f seconds\n", _noPulseTimeSecs); 
        } 

        //printf("%f %f %f %f\n", pulseValue, _movingAvg, _movingVariance / static_cast<double>(_cLagWindow), _movingStdDev);
    }

    return noutput_items;
}

#if 0
    pulse_detect_ff::sptr
    pulse_detect_ff::make(ff)
    {
      return gnuradio::get_initial_sptr
        (new pulse_detect_ff_impl(ff));
    }


    /*
     * The private constructor
     */
    pulse_detect_ff_impl::pulse_detect_ff_impl(ff)
      : gr::block("pulse_detect_ff",
              gr::io_signature::make(<+MIN_IN+>, <+MAX_IN+>, sizeof(<+ITYPE+>)),
              gr::io_signature::make(<+MIN_OUT+>, <+MAX_OUT+>, sizeof(<+OTYPE+>)))
    {}

    /*
     * Our virtual destructor.
     */
    pulse_detect_ff_impl::~pulse_detect_ff_impl()
    {
    }

    void
    pulse_detect_ff_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    pulse_detect_ff_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const <+ITYPE+> *in = (const <+ITYPE+> *) input_items[0];
      <+OTYPE+> *out = (<+OTYPE+> *) output_items[0];

      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }
#endif

  } /* namespace VHFPulseDetect2 */
} /* namespace gr */

