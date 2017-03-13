#! /usr/bin/env bash

systemlibs="build-essential libreadline-dev libgmp-dev liblapack-dev libblas-dev libncurses-dev libzmq3-dev libcurl4-gnutls-dev libopenblas-dev zlib1g-dev"
# get system packages
essentialpythons="python-dev python-pip python3-numpy python3-matplotlib python-tk"
compilers="gfortran g++"
editors="kate vim emacs"
miscs="git nodejs-legacy npm javascript-common julia r-base"

#
# install all required system packages
#
sudo apt-get update
for pack in $systemlibs $essentialpythons $compilers $editors $miscs
do
    sudo apt-get install --assume-yes $pack
done

#
# install some python2.7 libs. Using pip, we hope to get newer versions than by
# downloading the apt-get equivalents python-numpy, python-virtualenv, etc.
#
sudo pip install setuptools numpy scipy cython sklearn virtualenv matplotlib

#
# create a software directory
#
mkdir software
cd software

#
# get IPOPT and its third party libraries. Lapack and Blas are already installed above
#
wget https://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.7.tgz
tar xzf Ipopt-3.12.7.tgz
bash -c "cd Ipopt-3.12.7/ThirdParty/Mumps/ && ./get.Mumps"
bash -c "cd Ipopt-3.12.7/ThirdParty/ASL/ && ./get.ASL"
mkdir ipopt-build
bash -c "cd ipopt-build && ../Ipopt-3.12.7/configure && make && make install"


#
# get SCIP and compile the shared libscipopt for PySCIPOpt, together with IPOPT
#
wget http://scip.zib.de/download/release/scipoptsuite-4.0.0.tgz
tar xzf scipoptsuite-4.0.0.tgz
bash -c "cd scipoptsuite-4.0.0 && tar xzf scip-4.0.0.tgz"
bash -c "cd scipoptsuite-4.0.0 && mkdir -p scip-4.0.0/lib/static scip-4.0.0/lib/shared"
for libtype in static shared
do
	bash -c "cd scipoptsuite-4.0.0/scip-4.0.0/lib/${libtype} && ln -s ../../../../ipopt-build ipopt.linux.x86_64.gnu.opt"
done
for spx in spx1 spx2
do
	for static in false true
	do
		bash -c "cd scipoptsuite-4.0.0/scip-4.0.0/lib/ && touch linkscreated.${spx}-opt.linux.x86_64.gnu.true-opt.false-opt.${static}"
	done
done
bash -c "cd scipoptsuite-4.0.0 && make SHARED=true IPOPT=true ZIMPL=false scipoptlib"

#
# clone my PySCIPOpt fork with indicator and cardinality constraint support
#
git clone https://github.com/GregorCH/PySCIPOpt.git
bash -c "cd PySCIPOpt && git fetch origin && git checkout add-indicator-and-cardinality-constraint-support"
bash -c "cd PySCIPOpt && ln -s ../scipoptsuite-4.0.0/scip-4.0.0/src include && ln -s ../scipoptsuite-4.0.0/lib lib"
bash -c "cd PySCIPOpt && sudo python setup.py install"
