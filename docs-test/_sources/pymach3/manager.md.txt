# Manager

This module handles configuration and YAML access. Its main class is
{py:class}`pyMaCh3._pyMaCh3.manager.Manager`, the binding of
{cpp:class}`Manager`.

YAML access is similar to C++, but scalar values are exposed as strings by
{py:meth}`pyMaCh3._pyMaCh3.manager.YamlNode.data`. Convert them to the
appropriate Python type.

For example, consider this configuration:

```yaml
Example:
  Int: 1234
  Str: TestString
  IntArray: [0, 1, 2]
  StrArray: [val1, val2, val3]
```

In C++ you would access values using `node["Int"].as<int>()`,
`node["Str"].as<std::string>()`, or
`node["IntArray"].as<std::vector<int>>()`.

In Python:

```python
from pyMaCh3 import manager

node = manager.load_file("config.yaml")["Example"]
test_int = int(node["Int"].data())
test_str = node["Str"].data()

int1 = int(node["IntArray"][0].data())
int2 = int(node["IntArray"][1].data())
int3 = int(node["IntArray"][2].data())

str1 = node["StrArray"][0].data()
str2 = node["StrArray"][1].data()
str3 = node["StrArray"][2].data()
```

List comprehensions simplify access to sequences:

```python
int_list = [int(item.data()) for item in node["IntArray"]]
str_list = [item.data() for item in node["StrArray"]]
```

## API reference

```{eval-rst}
.. automodule:: pyMaCh3._pyMaCh3.manager
   :members:
   :undoc-members:
   :show-inheritance:
```
