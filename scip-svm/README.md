# SCIP SVM Example

This coding example uses the Python interface PySCIPOpt to model and train a sparse linear Support Vector Machine
for a simple classification task. In contrast to the very common use of L1 regularization
to enforce sparsity, the presented model models the sparse selection of features as a hard side constraint involving discrete (binary) variables to decide if a weight must be zero.

The implementation of these models can be used as an exercise by providing only the data-directory and the modules run.py, and SCIPSVMExercise.py. The third module SCIPSVMSolution.py implements the code of the solution.

The exercise requires to model two linear SVMs  with SCIP, a normal one without discrete variables (a standard linear SVM with soft margin and L2 regularization), and a second one that enforces sparsity through binary variables.

# The runner

The script run.py represents the user interface to this exercise. It can load the SVM models from the exercise or solution module. It will train and score both the linear and sparse linear SVM. It compares the results to a linear Support Vector classifier from the sklearn package to validate the model.

Execting
```
python run.py
```

should yield the following output:
```
linear          : Accuracy 0.344
sparselinear    : Accuracy 0.344
sklearn         : Accuracy 0.965
```

By replacing the line
```
from SCIPSVMExercise import SCIPSVMLinear, SCIPSVMSparseLinear
```

with
```
from SCIPSVMSolution import SCIPSVMLinear, SCIPSVMSparseLinear
```

the procedure should take about 10 seconds to run. The output will change to (concrete values might vary)
```
linear          : Accuracy 0.961
sparselinear    : Accuracy 0.944
sklearn         : Accuracy 0.965
```

# Prerequisites

For this exercise to work, it it is necessary to have PySCIPOpt importable from within python, ie, executing
```
 python -c "from pyscipopt import model; print(\"Good\")"
```
should output ```Good```, but no module import errors. Furthermore, in order to use PySCIPOpt properly, it should load a SCIP library that uses IPOPT internally to solve NLP relaxations. The installation of this toolchain is pretty custom, but an automated bash script for Linux can be found [in this repository](https://github.com/gregorch/springschool).

