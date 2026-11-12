# Plotting

The plotting module produces plots from MaCh3 outputs and supports comparing
results with other fitters. The
[Doxygen plotting guide](https://mach3-software.github.io/MaCh3/group__MaCh3Plotting.html)
describes the plotting configuration.

{py:class}`pyMaCh3._pyMaCh3.plotting.PlottingManager` provides high-level
access to the plotting library:

```python
import sys
from pyMaCh3 import plotting

man = plotting.PlottingManager()
man.parse_inputs(sys.argv)

# Use the manager to construct your plots.
```

The corresponding C++ class is {cpp:class}`M3::Plotting::PlottingManager`.

## API reference

```{eval-rst}
.. automodule:: pyMaCh3._pyMaCh3.plotting
   :members:
   :undoc-members:
   :show-inheritance:
```
