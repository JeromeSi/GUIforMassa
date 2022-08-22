#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  try_03_00.py
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
import json
import requests

class App:
    def __init__(self):
        self._initUI()

    def _initUI(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('../glade/try_03.glade')
        self.builder.connect_signals(self) # connect the signals added in the glade file
        self.window = self.builder.get_object('window_main')
        self.window.connect('destroy', Gtk.main_quit)
        self.whereIsNode()
        # ~ self.values()
        self.window.show_all()
        return 0

    def whereIsNode(self):
        requete = {}
        if os.path.isfile(os.environ['HOME']+'/.GUIforMassa-ini.toml'):
            self.parametersDictionnary = toml.load(os.environ['HOME']+'/.GUIforMassa-ini.toml')
            for theName in ('Folder','Password','Hostname','User'):
                self.builder.get_object('Entry_Massa_'+theName).set_text(self.parametersDictionnary['node'+theName])
            if self.parametersDictionnary['host'] == 'Local':
                self.builder.get_object('Radio_Local').set_active(True)
                self.commandBegin="cd "+self.parametersDictionnary['nodeFolder']+"massa-client;./massa-client -p "+self.parametersDictionnary['nodePassword']+" "
                self.urlPublic='http://127.0.0.1:33035'
                try:
                    requete = requests.post(self.urlPublic,data='{"jsonrpc": "2.0", "method": "get_status", "id": 124}',headers={"Content-Type": "application/json"})
                except Exception as e:
                    return
                if requete != {}:
                    self.dicoGetStatus = json.loads(requete.text)
            else:
                self.builder.get_object('Radio_Remote').set_active(True)
                self.commandBegin="ssh "+self.parametersDictionnary['nodeUser']+"@"+self.parametersDictionnary['nodeHostname']+" \"cd "+self.parametersDictionnary['nodeFolder']+"massa-client;./massa-client -p "+self.parametersDictionnary['nodePassword']+" "
                self.urlPublic = 'http://'+self.parametersDictionnary['nodeHostname']+':33035'
                try:
                    requete = requests.post(self.urlPublic,data='{"jsonrpc": "2.0", "method": "get_status", "id": 124}',headers={"Content-Type": "application/json"})
                except Exception as e:
                    self.builder.get_object('Label_status').set_text('Node is off or I can\'t join it')
                    return
                if requete != {}:
                    self.dicoGetStatus = json.loads(requete.text)
        else:
            self.parametersDictionnary = {}
        self.stakingAddress()
        self.values()
        self.builder.get_object('Label_status').set_text('Good news, node is on')
        return 0

    def stakingAddress(self):
        if self.builder.get_object('Radio_Local').get_active():
            reponse = requests.post(
                'http://127.0.0.1:33034',
                headers={"Content-Type": "application/json"},
                data='{"jsonrpc": "2.0","method": "get_staking_addresses","id": 0}')
            self.address=json.loads(reponse.text)['result'][0]
        else:
            commande="ssh "+self.parametersDictionnary['nodeUser']+"@"+self.parametersDictionnary['nodeHostname']+' \"curl -s -X POST -H \\\"Content-Type: application/json\\\" -d \'{\\\"jsonrpc\\\": \\\"2.0\\\", \\\"method\\\": \\\"get_staking_addresses\\\", \\\"id\\\": 123 }\' 127.0.0.1:33034\"'
            reponse = str(subprocess.run(commande,capture_output=True,shell=True).stdout)[2:-3]
            self.address=json.loads(reponse)['result'][0]
        self.builder.get_object('Label_TheAddress').set_text(self.address)
        return 0

    def values(self):
        if self.parametersDictionnary != {}:
            final = requests.post(
                self.urlPublic,
                headers={"Content-Type": "application/json"},
                data='{"jsonrpc": "2.0","method": "get_addresses","params": [["'+self.address+'"]],"id": 0}')
            info = json.loads(final.text)
            self.balanceValues(info)
            self.rollsValues(info)
            self.cyclesValues(info)
            self.connexionValues(self.dicoGetStatus)
        return 0

    def balanceValues(self,getAddresses):
        self.builder.get_object('Label_Balance_Final_Value').set_text(str(int(float(getAddresses['result'][0]['ledger_info']['final_ledger_info']['balance']))))
        self.builder.get_object('Label_Balance_Candidate_Value').set_text(str(int(float(getAddresses['result'][0]['ledger_info']['candidate_ledger_info']['balance']))))
        self.builder.get_object('Label_Balance_Locked_Value').set_text(str(int(float(getAddresses['result'][0]['ledger_info']['locked_balance']))))
        return 0

    def rollsValues(self,getAddresses):
        self.builder.get_object('Label_Rolls_Active_Value').set_text(str(getAddresses['result'][0]['rolls']['active_rolls']))
        self.builder.get_object('Label_Rolls_Final_Value').set_text(str(getAddresses['result'][0]['rolls']['final_rolls']))
        self.builder.get_object('Label_Rolls_Candidate_Value').set_text(str(getAddresses['result'][0]['rolls']['candidate_rolls']))
        return 0

    def cyclesValues(self,getAddresses):
        inOrder=[getAddresses['result'][0]['production_stats'][0]]
        cycleMin=getAddresses['result'][0]['production_stats'][0]['cycle']
        for i in range(1,len(getAddresses['result'][0]['production_stats'])):
            j=-1
            inOrder.append(getAddresses['result'][0]['production_stats'][i])
            while inOrder[j-1]['cycle'] < inOrder[j]['cycle'] and j > -len(inOrder)+1:
                temp=inOrder[j-1]
                inOrder[j-1]=inOrder[j]
                inOrder[j]=temp
                j=j-1
            if j == -len(inOrder)+1 and inOrder[j-1]['cycle'] < inOrder[j]['cycle']:
                temp=inOrder[0]
                inOrder[0]=inOrder[1]
                inOrder[1]=temp
        self.builder.get_object('Label_Current').set_text(str(inOrder[0]['cycle']))
        self.builder.get_object('Label_Produced_Current_value').set_text(str(inOrder[0]['ok_count']))
        self.builder.get_object('Label_Failed_Current_value').set_text(str(inOrder[0]['nok_count']))
        for i in range(1,5):
            self.builder.get_object('Label_Previous'+str(i)).set_text(str(inOrder[i]['cycle']))
            self.builder.get_object('Label_Produced_Previous'+str(i)+'_value').set_text(str(inOrder[i]['ok_count']))
            self.builder.get_object('Label_Failed_Previous'+str(i)+'_value').set_text(str(inOrder[i]['nok_count']))
        return 0

    def refreshDatas(self,widget):
        requete = {}
        try:
            requete = requests.post(self.urlPublic,data='{"jsonrpc": "2.0", "method": "get_status", "id": 124}',headers={"Content-Type": "application/json"})
        except Exception as e:
            self.builder.get_object('Label_status').set_text('Node is off or I can\'t join it')
            return
        if requete != {}:
            self.dicoGetStatus = json.loads(requete.text)
            self.stakingAddress()
            self.values()
            self.builder.get_object('Label_status').set_text('Good news, node is on')
        return 0

    def sellRolls(self,widget):
        numberOfRolls = self.builder.get_object('SpinButton_NumberofRolls').get_value_as_int()
        numberOfFees = self.builder.get_object('SpinButton_fees').get_value_as_int()
        if self.builder.get_object('Radio_Local').get_active():
            cmd = self.commandBegin+"sell_rolls "+self.address+" "+str(numberOfRolls)+" "+str(numberOfFees)
        else:
            cmd = self.commandBegin+"sell_rolls "+self.address+" "+str(numberOfRolls)+" "+str(numberOfFees)+"\""
        final = subprocess.run(cmd,capture_output=True,shell=True)
        return 0

    def buyRolls(self,widget):
        numberOfRolls = self.builder.get_object('SpinButton_NumberofRolls').get_value_as_int()
        numberOfFees = self.builder.get_object('SpinButton_fees').get_value_as_int()
        if self.builder.get_object('Radio_Local').get_active():
            cmd = self.commandBegin+"buy_rolls "+self.address+" "+str(numberOfRolls)+" "+str(numberOfFees)
        else:
            cmd = self.commandBegin+"buy_rolls "+self.address+" "+str(numberOfRolls)+" "+str(numberOfFees)+"\""
        final = subprocess.run(cmd,capture_output=True,shell=True)
        return 0

    def saveParameters(self,widget):
        requete = {}
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
            # ~ self.stakingAddress()
            # ~ self.builder.get_object('Label_TheAddress').set_text(self.address)
        lefichier = open(os.environ['HOME']+'/.GUIforMassa-ini.toml','w')
        datas = toml.dump(parametersDictionnary, lefichier)
        lefichier.close()
        self.whereIsNode()
        return 0

    def connexionValues(self,getStatus):
        self.builder.get_object('Label_Connexions_IN_Value').set_text(str(getStatus['result']['network_stats']['in_connection_count']))
        self.builder.get_object('Label_Connexions_OUT_value').set_text(str(getStatus['result']['network_stats']['out_connection_count']))
        return 0

    def destroyDialogBox_HowMany(self,widget):
        self.builder.get_object('DialogBox_HowMany').destroy()
        return 0


if __name__ == "__main__":
  main = App() # create an instance of our class
  Gtk.main() # run the darn thing
