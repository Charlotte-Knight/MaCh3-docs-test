# Sample handlers

This module evaluates the likelihood of an experimental model at different
parameter values, given your data.

Implement a sample handler derived from
{py:class}`pyMaCh3._pyMaCh3.samples.SampleHandlerBase` for the event samples
in your experiment. The underlying C++ classes
{cpp:class}`SampleHandlerBase` and {cpp:class}`SampleHandlerInterface`
describe the framework's sample-handling interfaces. Although the C++ and
Python method names differ, the same analysis concepts apply.

## API reference

```{eval-rst}
.. automodule:: pyMaCh3._pyMaCh3.samples
   :members:
   :undoc-members:
   :show-inheritance:
```
