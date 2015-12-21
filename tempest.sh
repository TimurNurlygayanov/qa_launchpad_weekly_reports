#rm -rf fuel-qa
#git clone https://github.com/openstack/fuel-qa.git
sudo pip install mock >= 1.0.1
sudo pip install pytest >= 2.7.1
sudo pip install pytest-django >= 2.8.0
sudo pip install factory_boy >= 2.4.1
sudo pip install lxml >= 3.4.4
sudo pip install pyyaml
sudo pip install launchpadlib
sudo pip install simplejson
export TESTRAIL_USER="obutenko@mirantis.com"
export TESTRAIL_PASSWORD="Ktyjxrf123"
export TESTRAIL_MILESTONE="8.0"
export TESTRAIL_TEST_SUITE="[8.0][MOSQA] Tempest 8.0"
export RELEASE="Ubuntu 14.04"
export ISO="317"
export TEST_RUN_NAME="Tempest - HA mode; Neutron with TUN; Cinder LVM"
#export TEST_RUN_NAME="Tempest - HA mode; Neutron with VLAN; Ceph volumes, images, eph. volumes"
python fuel-qa/fuelweb_test/testrail/report_tempest_results.py -r "$TEST_RUN_NAME" -c "${RELEASE}" -i "${ISO}" -p tempest-report.xml
