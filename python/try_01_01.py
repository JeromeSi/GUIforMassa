#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  try_01.py
#
#  Copyright 2022 Jerome Signouret <jerome.signouret le a entouré laposte.net>
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

import os
import subprocess
import toml

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
        if os.path.isfile(os.environ['HOME']+'/.GUIforMassa-ini.toml'):
            self.parametersDictionnary = toml.load(os.environ['HOME']+'/.GUIforMassa-ini.toml')
            self.nodeUser = self.parametersDictionnary['nodeUser']
            self.nodeName = self.parametersDictionnary['nodeHostname']
            self.nodeFolder = self.parametersDictionnary['nodeFolder']
            self.nodePassword = self.parametersDictionnary['nodePassword']
            for theName in ('Folder','Password','Hostname','User'):
                self.builder.get_object('Entry_Massa_'+theName).set_text(self.parametersDictionnary['node'+theName])
            if self.parametersDictionnary['host'] == 'Local':
                self.builder.get_object('Radio_Local').set_active(True)
                self.commandBegin="cd "+self.nodeFolder+"massa-client;./massa-client -p "+self.nodePassword+" "
            else:
                self.builder.get_object('Radio_Remote').set_active(True)
                self.commandBegin="ssh "+self.nodeUser+"@"+self.nodeName+" \"cd "+self.nodeFolder+"massa-client;./massa-client -p "+self.nodePassword+" "
            cmd=self.commandBegin+"wallet_info\""
            final = subprocess.run(cmd,capture_output=True,shell=True)
            info = str(final.stdout)[2:-1]
            self.address=info.split("\\n")[3].split(": ")[1]
        else:
            self.parametersDictionnary = {}

    def values(self):
        if self.parametersDictionnary != {}:
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

    def saveParameters(self,widget):
        parametersDictionnary = {}
        folder = self.builder.get_object('Entry_Massa_Folder').get_text()
        if folder[-1] != "/":
            self.builder.get_object('Entry_Massa_Folder').set_text(folder+"/")
        for theName in ('Folder','Password','Hostname','User'):
            parametersDictionnary['node'+theName] = self.builder.get_object('Entry_Massa_'+theName).get_text()
        if self.builder.get_object('Radio_Local').get_active():
            parametersDictionnary['host'] = 'Local'
        else:
            parametersDictionnary['host'] = 'Remote'
        lefichier = open(os.environ['HOME']+'/.GUIforMassa-ini.toml','w')
        datas = toml.dump(parametersDictionnary, lefichier)
        lefichier.close()
        self.whereIsNode()

    def connexionValues(self,getStatus):
        self.builder.get_object('Label_Connexions_IN_Value').set_text(getStatus.split("\\n")[38].split(": ")[1])
        self.builder.get_object('Label_Connexions_OUT_value').set_text(getStatus.split("\\n")[39].split(": ")[1])

    def on_window_main_destroy(self,fenetre):
        print("Quitter")
        # ~ Gtk.main_quit

if __name__ == "__main__":
  main = App() # create an instance of our class
  Gtk.main() # run the darn thing
