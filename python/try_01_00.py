#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  try_00.py
#
#  Copyright 2022 Jerome Signouret <jerome.signouret@ac-bordeaux.fr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import subprocess

class App:
    def __init__(self):
        self._initUI()

    def _initUI(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('../glade/try_01.glade')
        self.builder.connect_signals(self) # connect the signals added in the glade file
        self.window = self.builder.get_object('window_main')
        self.window.connect('destroy', Gtk.main_quit)
        self.whereIsNode()
        self.values()
        self.window.show_all()

    def whereIsNode(self):
        self.nodeUser="jerome"
        self.nodeName="nextcloud"
        self.nodeFolder="/home/jerome/massa/"
        self.passWord="massaggcom"
        self.commandBegin="ssh "+self.nodeUser+"@"+self.nodeName+" \"cd "+self.nodeFolder+"massa-client;./massa-client -p "+self.passWord+" "
        cmd=self.commandBegin+"wallet_info\""
        final = subprocess.run(cmd,capture_output=True,shell=True)
        info = str(final.stdout)[2:-1]
        self.address=info.split("\\n")[3].split(": ")[1]

    def values(self):
        cmd = self.commandBegin+"get_addresses "+self.address+"\""
        final = subprocess.run(cmd,capture_output=True,shell=True)
        info = str(final.stdout)[2:-1]
        self.balanceValues(info)
        self.rollsValues(info)
        self.cyclesValues(info)
        cmd = self.commandBegin+"get_status "+self.address+"\""
        final = subprocess.run(cmd,capture_output=True,shell=True)
        info = str(final.stdout)[2:-1]
        self.connexionValues(info)

    def balanceValues(self,getAddresses):
        self.builder.get_object('Label_Balance_Final_Value').set_text(str(int(float(getAddresses.split("\\n")[3].split(": ")[1]))))
        self.builder.get_object('Label_Balance_Candidate_Value').set_text(str(int(float(getAddresses.split("\\n")[4].split(": ")[1]))))
        self.builder.get_object('Label_Balance_Locked_Value').set_text(getAddresses.split("\\n")[5].split(": ")[1])

    def rollsValues(self,getAddresses):
        self.builder.get_object('Label_Rolls_Active_Value').set_text(getAddresses.split("\\n")[12].split(": ")[1])
        self.builder.get_object('Label_Rolls_Final_Value').set_text(getAddresses.split("\\n")[13].split(": ")[1])
        self.builder.get_object('Label_Rolls_Candidate_Value').set_text(getAddresses.split("\\n")[14].split(": ")[1])

    def cyclesValues(self,getAddresses):
        self.builder.get_object('Label_Current').set_text(getAddresses.split("\\n")[-3].split(" ")[8])
        self.builder.get_object('Label_Produced_Current_value').set_text(getAddresses.split("\\n")[-3].split(" ")[2])
        self.builder.get_object('Label_Failed_Current_value').set_text(getAddresses.split("\\n")[-3].split(" ")[5])
        for i in range(1,5):
            self.builder.get_object('Label_Previous'+str(i)).set_text(getAddresses.split("\\n")[-3-i].split(" ")[8])
            self.builder.get_object('Label_Produced_Previous'+str(i)+'_value').set_text(getAddresses.split("\\n")[-3-i].split(" ")[2])
            self.builder.get_object('Label_Failed_Previous'+str(i)+'_value').set_text(getAddresses.split("\\n")[-3-i].split(" ")[5])
    def refreshDatas(self,widget):
        self.values()

    def connexionValues(self,getStatus):
        self.builder.get_object('Label_Connexions_IN_Value').set_text(getStatus.split("\\n")[38].split(": ")[1])
        self.builder.get_object('Label_Connexions_OUT_value').set_text(getStatus.split("\\n")[39].split(": ")[1])

    def on_window_main_destroy(self,fenetre):
        print("Quitter")
        # ~ Gtk.main_quit

if __name__ == "__main__":
  main = App() # create an instance of our class
  Gtk.main() # run the darn thing
