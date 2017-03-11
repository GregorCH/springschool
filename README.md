# Spring School Ressources

Some Ressources and material for the [Spring School](http://optdata-springschool.com/index.php/en/) on Optimization and Data Science in Novi Sad.

# get-software

Bash Script to install system libraries, some site packages for Python
and specific optimization software (IPOPT, SCIP, PySCIPOpt, Julia).

Notes/CHANGELOG
-----

- 2017/Mar/11 In an earlier version of the script, I misspelled the packages "julia" and "build-essential". Either rerun the updated script,
or install these packages manually using
```
    sudo apt-get install build-essential julia
```

CAUTION
-------

This script permanently changes your overall system by using `sudo apt-get install` and `sudo pip install` commands.
It is therefore pretty invasive.


Updating the system packages (`sudo apt-get`) should be pretty safe. However, updating system python libraries may cause incompatibilities
with existing python projects.

For beginners, I recommend to
use the downloadable [Linux Mint virtual environment](www.zib.de/hendel/download/Linux_Mint_18.1_xfce.ova),
which you can load into, e.g., virtual box like [so](https://www.maketecheasier.com/import-export-ova-files-in-virtualbox/).


Intermediate and expert linux users can open the script and comment out the undesired parts.

The main part of this script is not the system library installation, but the installation of optimization software, which is,
allegedly, pretty nonstandard. Some of the system libraries, however, are required for the optimization packages to work.


Running the script
------------------

Launch the script in a debian based linux system (the commands `apt-get` and `wget` must exist),

```
./get-software.sh
```

The installation is fully automated and takes about 10 minutes.
The script requires root privileges (`sudo`) for the system.
The script creates a directory "software" under the current working directory,
into which IPOPT and SCIP are downloaded, setup, and compiled.


Testing the installation
------------------------

After executing the script, you can execute
```
software/scipoptsuite-4.0.0/scip-4.0.0/bin/scip
```

and should see the interactive shell of SCIP open:

```
SCIP version 4.0.0 [precision: 8 byte] [memory: block] [mode: optimized] [LP solver: SoPlex 3.0.0] [GitHash: 21a6d7a]
Copyright (C) 2002-2017 Konrad-Zuse-Zentrum fuer Informationstechnik Berlin (ZIB)

External codes:
  Readline 6.3         GNU library for command line editing (gnu.org/s/readline)
  SoPlex 3.0.0         Linear Programming Solver developed at Zuse Institute Berlin (soplex.zib.de) [GitHash: b760d03]
  CppAD 20160000.1     Algorithmic Differentiation of C++ algorithms developed by B. Bell (www.coin-or.org/CppAD)
  ZLIB 1.2.8           General purpose compression library by J. Gailly and M. Adler (zlib.net)
  GMP 5.1.3            GNU Multiple Precision Arithmetic Library developed by T. Granlund (gmplib.org)
  Ipopt 3.12.7         Interior Point Optimizer developed by A. Waechter et.al. (www.coin-or.org/Ipopt)

user parameter file <scip.set> not found - using default parameters

SCIP>
```

It is important that Ipopt appears in the list of external codes.
You can then close this interactive shell by entering "quit", followed by the return key.














