# GUIforMassa

First try to make a GUI for a Massa node in Python.

You need :

- Linux with :
  
  - Python 3
  
  - Library `gi`, `toml`, `os`, `subprocess`

- 2 files :
  
  - `GUIforMassa.py`
  
  - `GUIforMassa.glade`

- Execute file `GUIforMassa.py`

Notes :

v0.0.1. :

- On screen :
  
  - connexions IN/OUT
  
  - balance : Finale/Candidate/Locked
  
  - Rolls : Active/Final/Candidate
  
  - In line / Off line
  
  - Cycles with produced and failed blocks current and 4 previous like `get_status`
  
  - 2 buttons Buy rolls / Sell rolls
  
  - Preferences menu

- Features :
  
  - Buying / selling rolls
  
  - Interact with the node over SSH in LAN or local
