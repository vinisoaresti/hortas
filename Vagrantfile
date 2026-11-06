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

    vm1.vm.provision "shell", inline: <<-SHELL
      echo "=== Provisionando VM1 ==="
      export DEBIAN_FRONTEND=noninteractive
      apt-get update -y
      apt-get install -y curl wget
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

    vm2.vm.synced_folder ".", "/vagrant_data"

    vm2.vm.provision "shell", inline: <<-SHELL
      echo "=== Provisionando VM2 ==="
      export DEBIAN_FRONTEND=noninteractive
      apt-get update -y
      apt-get install -y python3 python3-pip python3-venv
      sudo -u vagrant python3 -m venv /home/vagrant/venv
      sudo -u vagrant /home/vagrant/venv/bin/pip install --upgrade pip
      sudo -u vagrant /home/vagrant/venv/bin/pip install -r /vagrant_data/requirements.txt

      cat <<EOF > /etc/systemd/system/hortas.service
[Unit]
Description=API de Gestao de Hortas Comunitarias
After=network.target

[Service]
User=vagrant
WorkingDirectory=/vagrant_data
Environment=PYTHONDONTWRITEBYTECODE=1
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/vagrant/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

      systemctl daemon-reload
      systemctl enable --now hortas.service
      echo "=== Servico hortas iniciado e habilitado na VM2 ==="
    SHELL
  end
end
