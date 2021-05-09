/* -*- c++ -*- */

#define VHFPULSEDETECT2_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "VHFPulseDetect2_swig_doc.i"

%{
#include "VHFPulseDetect2/pulse_detect_ff.h"
%}

%include "VHFPulseDetect2/pulse_detect_ff.h"
GR_SWIG_BLOCK_MAGIC2(VHFPulseDetect2, pulse_detect_ff);
