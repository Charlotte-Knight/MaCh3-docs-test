# The `mach3` command

`mach3` is MaCh3's command-line interface. It combines several processing and
diagnostic tools as subcommands:

- **`process`** analyses MCMC chains, including posterior distributions,
  correlations, credible intervals, and comparisons between chains.
- **`diag`** runs MCMC diagnostics, including autocorrelation calculations.
- **`penterm`** calculates penalty terms for selected parameters at each step.

After building and installing MaCh3, load its environment:

```sh
source build/bin/setup.MaCh3.sh
mach3 --help
```

Replace `build` with your build or installation directory. Each subcommand has
its own help, available without supplying input files:

```sh
mach3 process --help
mach3 diag --help
mach3 penterm --help
```

## Examples

Argument order differs between commands. For example:

```sh
mach3 process processing.yaml chain.root
mach3 process processing.yaml chain1.root "Fit 1" chain2.root "Fit 2"
mach3 diag chain.root diagnostics.yaml
mach3 penterm chain.root penalty.yaml
```

These are invocation examples, not ready-to-run analyses: supply your own ROOT
chain files and appropriate YAML configurations. Use the `ProcessMCMC`,
`DiagMCMC`, or `GetPenaltyTerm` configuration section for the corresponding
command. See also [MCMC convergence](mcmc-convergence.md).

## Plugins

Additional commands can be supplied by dynamic plugins configured through
`MACH3_PLUGINS`, a colon-separated list of plugin paths. When plugins are loaded,
`mach3 --help` lists their commands as well. The reference below deliberately
documents only the built-in commands.

## Generated command reference

The following help is captured from the compiled executable for the revision
being documented. Subcommands are discovered automatically from its help;
their argument descriptions and defaults come directly from the C++ parsers.
Only help commands are executed, not analyses.

```{mach3-help}
```
