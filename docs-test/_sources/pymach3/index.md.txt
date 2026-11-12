# pyMaCh3

pyMaCh3 provides Python bindings to MaCh3's C++ libraries. The guides below
introduce each module; their API references are generated from the compiled
bindings, including available signatures and docstrings.

Build MaCh3 with `-DMaCh3_PYTHON_ENABLED=ON`, then make the installed package
available to the Python interpreter you use for your analysis. For a standard
CMake build in `build/`, the package is installed in `build/pyMaCh3`, so add
`build/` to `PYTHONPATH`:

```sh
export PYTHONPATH="$PWD/build${PYTHONPATH:+:$PYTHONPATH}"
```

You can then import the public modules:

```python
from pyMaCh3 import manager, samples, splines, fitters, parameters, plotting
```

The generated reference uses their defining names, such as
`pyMaCh3._pyMaCh3.manager.Manager`. Normal analysis code can use
`manager.Manager` after the import above.

```{toctree}
:maxdepth: 2

manager
samples
splines
fitters
parameters
plotting
```
