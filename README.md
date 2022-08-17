# GUIforMassa

First try to make a GUI for a [Massa](massa.net) node in Python.

v0.0.1 work !

You need :

- Linux with :
  
  - Python 3 (`sudo apt install python3`)
  
  - Library `gi`, `toml` (use of `os`, `subprocess` but installed by default)
    (` sudo apt install python3-gi python3-toml `)
  
  - For remote use, install `openssh` and use ID (not password)

- 2 files :
  
  - [`GUIforMassa.py`](./GUIforMassa.py)
  
  - [`GUIforMassa.glade`](./GUIforMassa.glade)

- Execute file `GUIforMassa.py`

Notes :

v0.0.2. :

- automatically update values of the node

- 

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
