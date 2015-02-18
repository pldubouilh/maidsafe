# Provides a base Ubuntu (14.04) image with a Maidsafe Pythonic Implementation
FROM ubuntu:14.04
MAINTAINER Twisted Matrix Labs <twisted-python@twistedmatrix.com>

# Last build date - this can be updated whenever there are security updates so
# that everything is rebuilt
ENV security_updates_as_of 2014-07-06

# Install security updates and required packages
RUN apt-get update && \
apt-get -y upgrade && \
apt-get -y install -q build-essential git && \
apt-get -y install -q python-dev libffi-dev libssl-dev python-pip

# Install required python packages, and twisted
RUN pip install service_identity pycrypto && \
pip install twisted && \
cd ~ && git clone https://github.com/pldubouilh/maidsafe.git && cd maidsafe && \
pip install -e kademlia/ && \
mkdir reconstructed scrambled dht
CMD ["bash"]
