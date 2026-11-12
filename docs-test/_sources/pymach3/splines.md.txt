# Splines

This module provides utilities for spline parameters. See the
[user guide](../user-guide/splines.md) for background.

{py:class}`pyMaCh3._pyMaCh3.splines.ResponseFunction` represents an individual
response function. Choose its interpolation scheme using
{py:class}`pyMaCh3._pyMaCh3.splines.InterpolationType`.

```{image} ../_static/images/spline-examples.png
:width: 400
:alt: Examples of linear, TSpline3 and monotonic interpolation
```

Construct a response function from the knot positions, knot values, and
interpolation type:

```python
from pyMaCh3 import splines

TSpline3_response_1 = splines.ResponseFunction(
    [0.0, 1.0, 2.0], [1.0, 0.5, 2.0],
    splines.InterpolationType.Cubic_TSpline3,
)
linear_response_1 = splines.ResponseFunction(
    [10.0, 11.0, 12.0], [6.0, 0.0, 0.5],
    splines.InterpolationType.Linear,
)
TSpline3_response_2 = splines.ResponseFunction(
    [0.0, 1.0, 2.0], [2.0, 3.0, 0.0],
    splines.InterpolationType.Cubic_TSpline3,
)
linear_response_2 = splines.ResponseFunction(
    [10.0, 11.0, 12.0], [3.0, 0.0, 4.5],
    splines.InterpolationType.Linear,
)
```

## Event-by-event splines

{py:class}`pyMaCh3._pyMaCh3.splines.EventSplineMonolith` handles efficient
event-by-event spline reweighting. Construct response functions for each
event and parameter, then group them by event:

```python
monolith = splines.EventSplineMonolith([
    [TSpline3_response_1, linear_response_1],
    [TSpline3_response_2, linear_response_2],
])
```

This creates a handler for two events with two spline parameters.
Bind a NumPy array using
{py:meth}`pyMaCh3._pyMaCh3.splines.EventSplineMonolith.set_param_value_array`
to set parameter values without repeatedly copying them into C++:

```python
import numpy as np

n_parameters = 2
param_array = np.zeros((n_parameters,))
monolith.set_param_value_array(param_array)

param_array[0] = 0.5
param_array[1] = 11.042
```

```{warning}
Keep the bound array alive and do not replace it with a new array:

    param_array = np.array([0.5, 11.0])

That would replace your Python reference, not update the array bound to the
monolith. Update individual elements as above, or assign through a slice:

    param_array[...] = [0.5, 11.0]

This interface avoids unnecessary copying between Python and C++.
```

## API reference

```{eval-rst}
.. automodule:: pyMaCh3._pyMaCh3.splines
   :members:
   :undoc-members:
   :show-inheritance:
```
