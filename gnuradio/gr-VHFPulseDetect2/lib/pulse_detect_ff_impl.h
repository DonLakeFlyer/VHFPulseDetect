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

#ifndef INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_IMPL_H
#define INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_IMPL_H

#include <VHFPulseDetect2/pulse_detect_ff.h>

namespace gr {
  namespace VHFPulseDetect2 {

    class pulse_detect_ff_impl : public pulse_detect_ff
    {
     public:
        pulse_detect_ff_impl(float threshold, float pulseDuration, int sampleRate);
        ~pulse_detect_ff_impl();

        virtual float threshold() const { return _threshold; }
        virtual void set_threshold(float threshold) { _threshold = threshold; }

        virtual int pulseDuration() const { return _pulseDuration; }
        virtual void set_pulseDuration(int pulseDuration) { _pulseDuration = pulseDuration; }

        virtual int sampleRate() const { return _sampleRate; }
        virtual void set_sampleRate(int sampleRate) { _sampleRate = sampleRate; }

        // Where all the action really happens
        int work(int noutput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

     private:

        unsigned int _sampleCount       = 0;
        double  _sampleRate;
        float   _pulseDuration;
        int     _minSamplesForPulse;
        double  _noPulseTimeSecs        = 3;
        int     _pulseSampleCount       = 0;
        float   _pulseMax               = 0;
        double  _lastPulseSeconds       = 0;
        bool    _trackingPossiblePulse  = false;
        float   _threshold              = 3.57; // Probability of pulse every two seconds
        double  _movingAvg              = 0;
        double  _movingVariance         = 0;
        int     _cMovingWindow;
        int     _cLag;
        double* _rgMovingAvg            = NULL;
        double* _rgMovingStdDev         = NULL;
        double* _rgMovingAvgPart        = NULL;
        double* _rgMovingVariancePart   = NULL;
        int     _curMovingIndex         = 0;
    };

  } // namespace VHFPulseDetect2
} // namespace gr

#endif /* INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_IMPL_H */

