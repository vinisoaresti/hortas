# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.box_check_update = false

  config.vm.define "vm1" do |vm1|
    vm1.vm.hostname = "vm1"
    vm1.vm.network "private_network", ip: "192.168.56.10"
    vm1.vm.provider "virtualbox" do |vb|
      vb.name = "hortas-vm1"
      vb.memory = "1024"
      vb.cpus = 1
      vb.gui = false
    end

    vm1.vm.synced_folder "./ansible", "/home/vagrant/ansible",
      owner: "vagrant",
      group: "vagrant",
      mount_options: ["dmode=755", "fmode=644"]

    vm1.vm.provision "shell", inline: <<-SHELL
      echo "=== Provisionando VM1 (No de Controle Ansible) ==="
      export DEBIAN_FRONTEND=noninteractive
      apt-get update -y
      apt-get install -y ansible curl wget

      mkdir -p /etc/ansible
      ln -sf /home/vagrant/ansible/ansible.cfg /etc/ansible/ansible.cfg
      ln -sf /home/vagrant/ansible/hosts /etc/ansible/hosts

      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
      if [ ! -f /home/vagrant/.ssh/id_ed25519 ]; then
        ssh-keygen -t ed25519 -N "" -f /home/vagrant/.ssh/id_ed25519
      fi
      chown -R vagrant:vagrant /home/vagrant/.ssh
      chmod 600 /home/vagrant/.ssh/id_ed25519
      chmod 644 /home/vagrant/.ssh/id_ed25519.pub

      mkdir -p /vagrant/.vagrant
      cp /home/vagrant/.ssh/id_ed25519.pub /vagrant/.vagrant/ansible_id_ed25519.pub

      if [ -f /vagrant/.vagrant/machines/vm2/virtualbox/private_key ]; then
        cp /vagrant/.vagrant/machines/vm2/virtualbox/private_key /tmp/vm2_key
        chown vagrant:vagrant /tmp/vm2_key
        chmod 600 /tmp/vm2_key
        PUB_KEY=$(cat /home/vagrant/.ssh/id_ed25519.pub)
        sudo -u vagrant ssh -i /tmp/vm2_key -o StrictHostKeyChecking=no -o ConnectTimeout=3 \
          vagrant@192.168.56.11 \
          "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && (grep -qxF '$PUB_KEY' ~/.ssh/authorized_keys || echo '$PUB_KEY' >> ~/.ssh/authorized_keys)" \
          2>/dev/null || true
        rm -f /tmp/vm2_key
      fi

      echo "=== VM1 configurada com sucesso ==="
    SHELL
  end

  config.vm.define "vm2" do |vm2|
    vm2.vm.hostname = "vm2"
    vm2.vm.network "private_network", ip: "192.168.56.11"
    vm2.vm.provider "virtualbox" do |vb|
      vb.name = "hortas-vm2"
      vb.memory = "1024"
      vb.cpus = 1
      vb.gui = false
    end

    vm2.vm.provision "shell", inline: <<-SHELL
      echo "=== Provisionando VM2 (No Gerenciado pelo Ansible) ==="
      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
      touch /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys
      chown -R vagrant:vagrant /home/vagrant/.ssh

      if [ -f /vagrant/.vagrant/ansible_id_ed25519.pub ]; then
        PUB_KEY=$(cat /vagrant/.vagrant/ansible_id_ed25519.pub)
        grep -qxF "$PUB_KEY" /home/vagrant/.ssh/authorized_keys || echo "$PUB_KEY" >> /home/vagrant/.ssh/authorized_keys
      fi
      echo "=== VM2 pronta para configuracao via Ansible ==="
    SHELL
  end
end
