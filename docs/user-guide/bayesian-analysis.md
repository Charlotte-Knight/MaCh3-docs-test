# Bayesian Analysis

## Introduction

{cpp:class}`MCMCProcessor` processes MCMC output and produces validation plots.

## Posteriors
Marginalised posterior is the standard output of MCMC. PDF is mean, Gauss indicates Gaussian fit to posterior while HPD (Highest Posterior Density Point). In most cases parameter posteriors are Gaussian, then all 3 values would give the same result. However, the strength of MCMC is that there is no assumption about gaussiantiy, and it can handle non-Gaussian parameters.

<img width="350" src="https://github.com/user-attachments/assets/e77f7287-c71e-49c6-9f61-161fd54e4229">

This plot will all be produced when running ProcessMCMC.

## Parameter Plot
This plot is summarising 1D posteriors in more compact way. It is being printed by default. 1sigma errors are same as in 1D marginalised distribution.

<img width="350" src="https://github.com/user-attachments/assets/37c15953-1926-44a4-9a87-d232ba2aaf06">

Since these plots are often targeted for publication, there is a tool called **GetPosftitParams** which make this plot with ability group parameter in whatever fashion you like. You can read more [here](https://github.com/mach3-software/MaCh3/wiki/15.-Plotting)

## Credible Intervals
This plot helps to tell which values are excluded based on X-credible intervals.

<img width="350" src="https://github.com/user-attachments/assets/2199f9ff-1901-4f7f-a5e8-43433049027e">

To produce, make sure the following field is true.
```
ProcessMCMC:
  MakeCredibleIntervals: true
```

## 2D Posteriors
Up to this point, we discussed marginalisation of posterior distribution into 1D.
It is possible to produce 2D marginalised posterior distribution. They are very useful to identify if parameters are correlated or not. In this example, there are strong correlations.

<img width="350" src="https://github.com/user-attachments/assets/91bb1c28-e3a5-4418-a077-ad9b968a29b5">

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

<img width="350" src="https://github.com/user-attachments/assets/fccae6a7-d18b-455f-9ed7-a413cc6eb746">

```
ProcessMCMC:
  PlotCorr: true
  MakeCredibleRegions: true
```

## Correlation Matrix
Based on 2D posterior distribution one can easily calculate correlation factor.
By calculating correlation factor between each combination of parameters we create a correlation matrix etc.

Example of such a matrix can be seen below.

<img width="350" src="https://github.com/user-attachments/assets/71d4eacd-10f8-4738-b32c-4de6a6d6a3a3">

Since for many parameters such matrices are unreadable, we also produce correlation for each parameter.
This allows more easily to see with what are the largest correlations for a given parameter.

<img width="350" src="https://github.com/user-attachments/assets/a77f7e24-e381-46f5-b924-f6e034676b74">

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

<img width="350" src="https://github.com/user-attachments/assets/06322f8e-8a4f-4ce4-81bb-e8865e1e47e9">

## Violin plot
This plot includes posterior distribution and mirrored reflection for each parameter.
Similar Parameter Plot, but it actually shows shape of distribution.

<img width="350" src="https://github.com/user-attachments/assets/168c224d-11bc-45c9-a3a6-416d878cfbe9">

```
ProcessMCMC:
  PlotCorr: true
  MakeViolin: true
```

## Ridgeline plot
This is yet another way of presents posteriors in a compact way. Very similar conceptually to violin plot.
Matter of taste which you prefer.

<img width="350" src="https://github.com/user-attachments/assets/42f9e914-05df-4d58-86de-7509bf6b63ce" />

## Bayes factor and Savage-Dickey
It is possible to obtain the Bayes factor for different hypothesis
```
  BayesFactor:
    # Goes as follows: ParamName Name[Model 1, Model 2], Model1[lower, upper ], Model2[lower, upper ]
    - ["sin2th_23", ["LO", "UO"], [0, 0.5], [0.5, 1]]
```

<img width="350" src="https://github.com/user-attachments/assets/258d88c5-5dc0-4e69-a1ce-282918570737">

or calculate savage Dickey, which is Bayes factor for point-like hypothesis
```
  SavageDickey:
    - ["Alpha_q3", 0.0001, [0, 1]]
```
<img width="350" src="https://github.com/user-attachments/assets/c021450b-7634-4e18-b9d6-fd2695a6a3e4">

## Parameter Evolution
```
  ParameterEvolution:
    - ["Norm_Param_0", 20]
```
Select parameter name and how many frames you want. The more, the longer it takes, so be careful

<img width="350" src="https://github.com/user-attachments/assets/84fce0eb-450f-437b-904f-9123300c3cf8">

## Bipolar plot

<img width="350" src="https://github.com/user-attachments/assets/a1c9b296-e05e-4d3e-8923-f39e2704f759">

## Reweighting
Chain reweighting is a technique allowing to test different priors without having to rerun fits.
This is especially useful when we want to test the impact of priors coming from reactor constraints.
Since we keep information on every step, reweight is calculated as ratio of new penalty term to original.

An example of default and original chain can be seen below. It should be noted that reweighting from PDG 2023 to flat prior
is impossible, as we would be missing phase-space to reweight. Thus, it is safer to run flat prior and reweight to
for example, 2023 PDG

<img width="350" src="https://github.com/user-attachments/assets/c3e58df2-13f9-4354-9450-a77e157831f1" />

## Oscillation Parameters Only
### Jarlskog Invariant

<img width="350" src="https://github.com/user-attachments/assets/9341f923-6609-4028-9bf0-3d8c51f6d399">

### Pie Plot (Clock Plot)

<img width="350" src="https://github.com/user-attachments/assets/8d79e996-0079-43c1-9139-e810c61a4298">

### PMNS Elements

<img width="350" src="https://github.com/user-attachments/assets/38f81567-9588-406c-9854-efcb97929db4">

### Unitarity Triangle

<img width="350" src="https://github.com/user-attachments/assets/bf92041a-59f1-4d5f-9edf-958b505b00e9">
