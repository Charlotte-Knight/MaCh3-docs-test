# Bayesian Analysis

## Introduction

{cpp:class}`MCMCProcessor` processes MCMC output and produces validation plots.

## Posteriors
Marginalised posterior is the standard output of MCMC. PDF is mean, Gauss indicates Gaussian fit to posterior while HPD (Highest Posterior Density Point). In most cases parameter posteriors are Gaussian, then all 3 values would give the same result. However, the strength of MCMC is that there is no assumption about gaussiantiy, and it can handle non-Gaussian parameters.

<img width="350" src="../_static/images/bayesian-analysis-01.png">

This plot will all be produced when running ProcessMCMC.

## Parameter Plot
This plot is summarising 1D posteriors in more compact way. It is being printed by default. 1sigma errors are same as in 1D marginalised distribution.

<img width="350" src="../_static/images/bayesian-analysis-02.png">

Since these plots are often targeted for publication, there is a tool called **GetPosftitParams** which make this plot with ability group parameter in whatever fashion you like. You can read more [here](https://github.com/mach3-software/MaCh3/wiki/15.-Plotting)

## Credible Intervals
This plot helps to tell which values are excluded based on X-credible intervals.

<img width="350" src="../_static/images/bayesian-analysis-03.png">

To produce, make sure the following field is true.
```
ProcessMCMC:
  MakeCredibleIntervals: true
```

## 2D Posteriors
Up to this point, we discussed marginalisation of posterior distribution into 1D.
It is possible to produce 2D marginalised posterior distribution. They are very useful to identify if parameters are correlated or not. In this example, there are strong correlations.

<img width="350" src="../_static/images/bayesian-analysis-04.png">

This can take some time, though. There are two ways: faster (using multithreading) but requiring lots of RAM, or slower but without RAM requirements. Once you obtain 2D posteriors, you can produce multiple additional plots.

To enable, this option must be on.
```
ProcessMCMC:
  PlotCorr: true
```

### Threshold
Not every 2D plot will be made. MaCh3 uses configurable threshold to print only more interesting plot. Threshold applies to correlation factor.
```
ProcessMCMC:
  Post2DPlotThreshold: 0.2
```

## Credible Region

<img width="350" src="../_static/images/bayesian-analysis-05.png">

```
ProcessMCMC:
  PlotCorr: true
  MakeCredibleRegions: true
```

## Correlation Matrix
Based on 2D posterior distribution one can easily calculate correlation factor.
By calculating correlation factor between each combination of parameters we create a correlation matrix etc.

Example of such a matrix can be seen below.

<img width="350" src="../_static/images/bayesian-analysis-06.png">

Since for many parameters such matrices are unreadable, we also produce correlation for each parameter.
This allows more easily to see with what are the largest correlations for a given parameter.

<img width="350" src="../_static/images/bayesian-analysis-07.png">

## Triangle plot
Triangle plot contains both 1D posterior and 2D posterior for a set of parameters.
```
  TrianglePlot:
    - ["Test", ["Norm_Param_0", "Norm_Param_1", "Spline_Param_0", "Spline_Param_1"]]
```
You can specify as many parameters as you like. But also as many combinations as you like
```
  TrianglePlot:
    - ["Test", ["Norm_Param_0", "Norm_Param_1", "Spline_Param_0", "Spline_Param_1"]]
    - ["Test2", ["Norm_Param_0", "Norm_Param_1"]]
```

<img width="350" src="../_static/images/bayesian-analysis-08.png">

## Violin plot
This plot includes posterior distribution and mirrored reflection for each parameter.
Similar Parameter Plot, but it actually shows shape of distribution.

<img width="350" src="../_static/images/bayesian-analysis-09.png">

```
ProcessMCMC:
  PlotCorr: true
  MakeViolin: true
```

## Ridgeline plot
This is yet another way of presents posteriors in a compact way. Very similar conceptually to violin plot.
Matter of taste which you prefer.

<img width="350" src="../_static/images/bayesian-analysis-10.png" />

## Bayes factor and Savage-Dickey
It is possible to obtain the Bayes factor for different hypothesis
```
  BayesFactor:
    # Goes as follows: ParamName Name[Model 1, Model 2], Model1[lower, upper ], Model2[lower, upper ]
    - ["sin2th_23", ["LO", "UO"], [0, 0.5], [0.5, 1]]
```

<img width="350" src="../_static/images/bayesian-analysis-11.png">

or calculate savage Dickey, which is Bayes factor for point-like hypothesis
```
  SavageDickey:
    - ["Alpha_q3", 0.0001, [0, 1]]
```
<img width="350" src="../_static/images/bayesian-analysis-12.png">

## Parameter Evolution
```
  ParameterEvolution:
    - ["Norm_Param_0", 20]
```
Select parameter name and how many frames you want. The more, the longer it takes, so be careful

<img width="350" src="../_static/images/bayesian-analysis-13.gif">

## Bipolar plot

<img width="350" src="../_static/images/bayesian-analysis-14.png">

## Reweighting
Chain reweighting is a technique allowing to test different priors without having to rerun fits.
This is especially useful when we want to test the impact of priors coming from reactor constraints.
Since we keep information on every step, reweight is calculated as ratio of new penalty term to original.

An example of default and original chain can be seen below. It should be noted that reweighting from PDG 2023 to flat prior
is impossible, as we would be missing phase-space to reweight. Thus, it is safer to run flat prior and reweight to
for example, 2023 PDG

<img width="350" src="../_static/images/bayesian-analysis-15.png" />

## Oscillation Parameters Only
### Jarlskog Invariant

<img width="350" src="../_static/images/bayesian-analysis-16.png">

### Pie Plot (Clock Plot)

<img width="350" src="../_static/images/bayesian-analysis-17.png">

### PMNS Elements

<img width="350" src="../_static/images/bayesian-analysis-18.png">

### Unitarity Triangle

<img width="350" src="../_static/images/bayesian-analysis-19.png">
