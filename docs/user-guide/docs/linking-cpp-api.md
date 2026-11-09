# Linking to C++ API entities

Use Sphinx's C++ domain roles in MyST Markdown:

```md
{cpp:class}`ParameterHandlerGeneric`
{cpp:func}`ParameterHandlerBase::GetNumParams`
```

For overloaded functions, include the full parameter types (and qualifiers) in
the role target so Sphinx can select the intended overload. Cross-reference
targets use the C++ name, not the header filename.

For example, the overload taking a group name and values is
{cpp:func}`void ParameterHandlerGeneric::SetGroupOnlyParameters(const std::string&, const std::vector<double>&)`.
