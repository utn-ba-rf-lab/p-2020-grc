#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-howto author.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy
from gnuradio import gr

class pf_2020(gr.sync_block):
    """
    docstring for block pf_2020
    """
    def __init__(self, modulation_key, psk_key, fc_key, fs_key, pammethod_key, pamtype_key, duty_key,
                nbits_key, am_fc_8bits_key, am_fc_7bits_key, am_fc_6bits_key, am_fc_5bits_key, psk_fc_key, psk_fs5M_key, psk_fs1M_key):

        gr.sync_block.__init__(self,
            name="pf_2020",
            #in_sig=numpy.float32,
            in_sig=None,
            out_sig=None)

        # Atributos
        self.modulation  = modulation_key;
        self.psk_mod = psk_key
        self.fc = fc_key
        self.fs = int(fs_key)
        self.duty = duty_key
        self.pam_methode = pammethod_key
        self.pam_type = pamtype_key
        self.am_nbits = nbits_key
        self.am_fc_8bits = am_fc_8bits_key
        self.am_fc_7bits = am_fc_7bits_key
        self.am_fc_6bits = am_fc_6bits_key
        self.am_fc_5bits = am_fc_5bits_key
        self.psk_fc = psk_fc_key
        self.psk_fs = 25e3
        self.psk_fs5M = psk_fs5M_key
        self.psk_fs1M = psk_fs1M_key
        self.pll = 120
        self.synthesize = True

        
        
        print("Modulation type: {}".format(self.modulation))
        print("PSK type: {}".format(self.psk_mod))
        print("Carrier: {} MHz".format(self.fc))
        print("Sampling frequency: {} MHz ".format(self.fs))
        print("Duty: {}".format(self.duty))
        print("PAM method: {}".format(self.pam_methode))
        print("PAM Type: {}".format(self.pam_type))
        print("N bits: {}".format(self.am_nbits))
        print("AM FC 8bits: {} MHz".format(self.am_fc_8bits))
        print("AM FC 7bits: {} MHz".format(self.am_fc_7bits))
        print("AM FC 6bits: {} MHz".format(self.am_fc_5bits))
        print("AM FC 5bits: {} MHz".format(self.psk_fc))
        print("PSK FS 5M: {}".format(self.psk_fs5M))
        print("PSK FS 1M: {}".format(self.psk_fs1M))


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return 

