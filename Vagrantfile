# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |v|
    v.name = "medaCy_demo_box"
    v.gui = false
    v.memory = 3000
    v.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
apt-get update
apt-get install -y python3 python3-pip python3-dev
python3 -m pip install --upgrade pip
pip3 install flask
pip3 install git+https://github.com/swfarnsworth/medaCy.git@development
pip3 install git+https://github.com/NLPatVCU/medaCy_model_clinical_notes.git
pip3 install git+https://github.com/swfarnsworth/medaCy_model_FDA_nanodrug_labels.git
python3 -u /vagrant/app.py
SHELL
end