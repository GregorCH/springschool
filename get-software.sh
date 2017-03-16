#! /usr/bin/env bash

systemlibs="build-essential libreadline-dev libgmp-dev liblapack-dev libblas-dev libncurses-dev libzmq3-dev libcurl4-gnutls-dev libopenblas-dev zlib1g-dev"
# get system packages
essentialpythons="python-dev python-pip python3-numpy python3-matplotlib python-tk"
compilers="gfortran g++"
editors="kate vim emacs"
miscs="git nodejs-legacy npm javascript-common julia r-base"

#
# install mx net
#
function installMxnet {
    # Clone mxnet repository. In terminal, run the commands WITHOUT "sudo"
    git clone https://github.com/dmlc/mxnet.git mxnet --recursive

    # If building with GPU, add configurations to config.mk file:
    cd mxnet
    cp make/config.mk .
    echo "USE_CUDA=0" >>config.mk
    echo "USE_CUDA_PATH=/usr/local/cuda" >>config.mk
    echo "USE_CUDNN=0" >>config.mk

    # Install MXNet for Python with all required dependencies
    cd setup-utils
    bash install-mxnet-ubuntu-python.sh

    # We have added MXNet Python package path in your ~/.bashrc.
    # Run the following command to refresh environment variables.
    echo "MXNet Python package path in your ~/.bashrc. Consider running"
    echo "  source ~/.bashrc"
    echo "to pick it up."
}

#
# installs Jupyter Notebook together with Julia, SparQL, and R kernels
#
function installJupyterNotebook {
virtualenv jupyter-venv
source jupyter-venv/bin/activate

git clone git://github.com/jupyter/notebook.git
cd notebook
pip install --pre -e .

jupyter --version
# Output: 4.0.6
#install sparqlkernel
pip install sparqlkernel
# tensorflow
pip install --upgrade tensorflow

jupyter sparqlkernel install
# install julia
julia <<EOF
Pkg.add("IJulia")
EOF
#install IRkernel
echo "R_LIBS=${HOME}/.local/R/" >> ~/.Renviron
mkdir -p ~/.local/R
R --save <<EOF
install.packages(c('crayon', 'pbdZMQ', 'devtools'),repos = "http://cran.de.r-project.org")
devtools::install_github(paste0('IRkernel/', c('repr', 'IRdisplay', 'IRkernel')))
IRkernel::installspec()
EOF

pip install matplotlib

#
# leave virtual environment
#
deactivate
}

function installScipIpoptPyscipopt {
#
# get IPOPT and its third party libraries. Get Lapack and Blas again, the system libraries have inconsistencies
#
wget https://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.7.tgz
tar xzf Ipopt-3.12.7.tgz
for thirdparty in Mumps ASL Lapack Blas
do
    bash -c "cd Ipopt-3.12.7/ThirdParty/$thirdparty/ && ./get.$thirdparty"
done
mkdir ipopt-build
bash -c "cd ipopt-build && ../Ipopt-3.12.7/configure && make -j && make install"


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
bash -c "cd scipoptsuite-4.0.0 && make SHARED=true IPOPT=true ZIMPL=false scipoptlib -j"

#
# clone my PySCIPOpt fork with indicator and cardinality constraint support
#
git clone https://github.com/GregorCH/PySCIPOpt.git
bash -c "cd PySCIPOpt && git fetch origin && git checkout add-indicator-and-cardinality-constraint-support"
bash -c "cd PySCIPOpt && ln -s ../scipoptsuite-4.0.0/scip-4.0.0/src include && ln -s ../scipoptsuite-4.0.0/lib lib"
bash -c "cd PySCIPOpt && sudo python setup.py install"
}

#
# install all required system packages
#
sudo apt-get update
for pack in $systemlibs $essentialpythons $compilers $editors $miscs
do
    sudo apt-get install --assume-yes $pack
done

sudo -H pip install --upgrade pip
sudo -H pip install setuptools
#
# install some python2.7 libs. Using pip, we hope to get newer versions than by
# downloading the apt-get equivalents python-numpy, python-virtualenv, etc.
#
sudo -H pip install numpy scipy cython sklearn virtualenv matplotlib

#

#
# create a software directory
#
mkdir software
cd software


# install the Jupyter notebook stuff
installJupyterNotebook

# install the mxnet stuff
#installMxnet

installScipIpoptPyscipopt

source ~/.bashrc
