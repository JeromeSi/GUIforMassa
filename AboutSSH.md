About SSH

Install ssh server on the node

- `sudo apt install openssh-server`

Install ssh client and use ID

- `sudo apt install openssh-client` (install ssh client)

- `ssh-keygen -t ed25519`(generate a key use to authification with server)

- `ssh-copy-id theuser@thenode`(install the key on the node)

That's done
