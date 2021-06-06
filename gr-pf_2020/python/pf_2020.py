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
import numpy as np
import subprocess
import shlex
import serial

from serial import Serial
from numpy import log, zeros, abs, sign


from gnuradio import gr


# Some constants to make the code performancer
A = 87.6
INV_A = np.float32(1/A)
INV_DIV_A = 1/(1+log(A))

MU = 255



class pf_2020(gr.sync_block):
    """
    docstring for block pf_2020
    """
    def __init__(self, modulation_key, psk_key, fc_key, fs_key, pammethod_key, pamtype_key, duty_key,
                nbits_key, am_fc_8bits_key, am_fc_7bits_key, am_fc_6bits_key, am_fc_5bits_key, psk_fc_key, psk_fs5M_key, psk_fs1M_key):

        gr.sync_block.__init__(self,
            name="pf_2020",
            in_sig=[numpy.float32],
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


        # Dafault values for configuration parameters.
        parameter01 = 1;
        parameter02 = 255;
        parameter03 = 8;
        parameter04 = 4;
        modulation_number  = 0;


        # Choosing PLL
        if(self.modulation == "am"):
            if(self.am_nbits == 8):
                if(self.am_fc_8bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_8bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_8bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 7):
                if(self.am_fc_7bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_7bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_7bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 6):
                if(self.am_fc_6bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_6bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_6bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 5):
                if(self.am_fc_5bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_5bits == "pll_100.5"):
                    self.pll = 100.5

            print("[INFO] | PLL: {} MHz \n[INFO] | Bits: {}".format(self.pll, self.am_nbits))
        
        else:
            self.pll = 120
            print("[INFO] | PLL: {} MHz".format(self.pll))



        if(self.modulation == "psk"):
            if(self.psk_fc == 5e6):
                self.psk_fs = self.psk_fs5M 
            else:
                self.psk_fs = self.psk_fs1M 



        # Check routine for re-synthesis

        try:

            f = open("../check_syn","r")
            rl = f.readline()
            # current = "{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,ammethod_key,pamtype_key,duty_key)
            current = "{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key)
            if (rl == current):
                self.synthesize = False
            else:
              f.close()
              f = open("check_syn", "w+")
              # f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,ammethod_key,pamtype_key,duty_key))
              f.write("{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key))
   
        except:
            print("[DEBUG] | Running exception code: the \"check_syn\" file doesn't exist")
            f = open("check_syn", "w+")
            # f.write("{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, pammethod_key, pamtype_key, duty_key))
            f.write("{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key))
            f.close()

        if(self.synthesize == True): 

            if(self.modulation == "am"):
                parameter01 = 1
                parameter02 = pow(2,self.am_nbits) -1 ;
                parameter03 = self.am_nbits;                
                modulation_number  = 1

                
                parameter04 = np.round(self.pll * 1e6 / (parameter02+1) / fs_key)-1;
                
                print("[INFO] | AM modulation is set");
    
            elif(self.modulation == "ook"):
                parameter02 = 2;

                print("[INFO] | OOK modulation is set");
    
            elif(self.modulation == "pam"):
                parameter01 = 1250                              # Divisor de frecuencia: fs = f_pll/parameter01 = 120MHz/1200 = 100kHz
                parameter02 = 12;   # VER!!!!!!!  NO SÉ SI ERA 12 O 24!!!!!!!!  Con 24 anda bien. Ver comportamiento con 12.
                parameter03 = 24;                               # Bits del DAC
                modulation_number  = 2

                print("[INFO] | PAM modulation is set");
    
            elif(self.modulation == "psk"):

                parameter04 = self.psk_fc/self.psk_fs;

                if(psk_key == "bpsk"):
                    parameter01 = 120e6/(2*self.psk_fc);
                    parameter02 = 2;
                    modulation_number = 3

                    print("[INFO] | BPSK modulation is set");
        
                elif(psk_key == "qpsk"):
                    parameter01 = 120e6/(4*self.psk_fc);
                    parameter02 = 4;
                    modulation_number = 4
                    print("[INFO] | QPSK modulation is set");
        
                elif(psk_key == "8psk"):
                    parameter01 = 120e6/(8*self.psk_fc);
                    parameter02 = 8;
                    modulation_number = 5
       
                    print("[INFO] | 8-PSK modulation is set");
    

            # Genera el archivo con los parámetros configurables de los .v
            self.modulatorParametersGenerator(parameter01, parameter02, parameter03, parameter04, modulation_number)
            
            # Descomentar para programar la FPGA
            # Dos rutas diferentes de lo mismo. Depende si corrés desde docker o a pedal
#            self.programFPGA("../../syn", "all")           # From docker
            # self.programFPGA("../../hdl/syn", "all")        # A pedal



            self.tty = serial.Serial('/dev/pts/3')



    def work(self, input_items, output_items):
        in0 = input_items[0]
#        b = np.uint8(in0*127-128)
        b = np.uint8(74)

        self.tty.write(b.tobytes())
        return 0




    ####
    # programFPGA
    #
    # This function runs the Makefile to make the synthesys, place and route and
    # programmation of the FPGA
    ####
   
    def programFPGA(self, pathMakefileHDL, target):
      subprocess.call(['make', '-C', pathMakefileHDL,'clean'])
      subprocess.call(['make', '-C', pathMakefileHDL, target, 'MOD={}'.format(self.modulation), 'PLL={}'.format(self.pll)])
      subprocess.call(['make', '-C', pathMakefileHDL, target, 'prog'])


    ####
    # modulatorParametersGenerator
    #
    # Used to write the necessary defines to build every modulator
    ####
    
    def modulatorParametersGenerator(self, parameter01, parameter02, parameter03, parameter04, modulation_number):
        # open file and write header
        f = open("../module_params.v","w+")
        #f = open("../../hdl/inc/module_params.v","w+")
        f.write("`ifndef __PROJECT_CONFIG_V\n`define __PROJECT_CONFIG_V\n\n")
        f.write("`define PARAMETER01 %d\n" % parameter01)
        f.write("`define PARAMETER02 %d\n" % parameter02)
        f.write("`define PARAMETER03 %d\n" % parameter03)
        f.write("`define PARAMETER04 %d\n" % parameter04)
        f.write("`define MODULATION %d\n" % modulation_number)
        f.write("`define CLK_PERIOD %d\n" % 4)
        f.write("\n`endif")
        f.close()



