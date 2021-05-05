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

#ifndef INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_H
#define INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_H

#include <VHFPulseDetect2/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace VHFPulseDetect2 {

    /*!
     * \brief <+description of block+>
     * \ingroup VHFPulseDetect2
     *
     */
    class VHFPULSEDETECT2_API pulse_detect_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<pulse_detect_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of VHFPulseDetect2::pulse_detect_ff.
       *
       * To avoid accidental use of raw pointers, VHFPulseDetect2::pulse_detect_ff's
       * constructor is in a private implementation
       * class. VHFPulseDetect2::pulse_detect_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(float threshold, float pulseDuration, int sampleRate);

      virtual float threshold() const = 0;
      virtual void set_threshold(float threshold) = 0;

      virtual int pulseDuration() const = 0;
      virtual void set_pulseDuration(int pulseDuration) = 0;

      virtual int sampleRate() const = 0;
      virtual void set_sampleRate(int sampleRate) = 0;
    };

  } // namespace VHFPulseDetect2
} // namespace gr

#endif /* INCLUDED_VHFPULSEDETECT2_PULSE_DETECT_FF_H */

