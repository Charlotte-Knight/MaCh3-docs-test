# Posterior Predictive

## Prior and Posterior Predictive Distributions

We consider the predictive distributions of the number of events $Z$. The prior
predictive distribution of $Z$ is given by:

$$
p(Z) = \int_{\vec{\theta}} p(\vec{\theta}) \, p(Z \mid \vec{\theta}) \, d\vec{\theta}.
$$

where $p(\vec{\theta})$ is the same prior probability as in Bayes' theorem. We
use the following procedure to obtain the prior predictive distribution:

1. Throw values of the parameters using their prior distributions.
2. Reweight MC to the selected parameters values. Reweighted MC is usually called a toy MC.
3. From multiple toy MCs, we obtain the mean value of the number of events \(Z\).

After the fit, we can predict the observable $Z_{\mathrm{pred}}$, which
estimates the expected measurement of the same physical process as $Z$. This is
known as the posterior predictive distribution
$p(Z_{\mathrm{pred}} \mid Z)$ (see [Bayesian analysis](bayesian-analysis.md)):

$$
p(Z_{\mathrm{pred}} \mid Z) = \int_{\vec{\theta}} p(Z_{\mathrm{pred}} \mid \vec{\theta}) \, p(\vec{\theta} \mid Z) \, d\vec{\theta}.
$$

where $p(\vec{\theta} \mid Z)$ is the posterior probability. We obtain the
posterior predictive distribution with the following steps:

1. Sample the posterior probability distribution by randomly selecting steps,
   to get $\vec{\theta}$ associated with the selected step.
2. Reweight MC to the selected parameters values.
3. From multiple toy MCs, we obtain the mean value of the number of events
   $Z_{\mathrm{pred}}$.

Figure shows the prior and posterior predictive distributions of the number of events. The prior predictive distribution is very wide compared to the posterior predictive distribution, and the relative error on the number of events for this sample has been reduced from 14\% to 0.7\%, which demonstrates how fit can reduce uncertainties.


<img width="60%" alt="Prior and posterior predictive distributions" src="https://github.com/user-attachments/assets/eee1c0bb-b14a-4f1f-9063-3e84f7a3ab12" />

This technique is visualised in following animation:

<video controls autoplay loop muted playsinline style="width: 50%;">
    <source src="https://raw.githubusercontent.com/KSkwarczynski/Python/main/MaCh3/animation/posterior_predictive_Example.mp4" type="video/mp4">
</video>

## Posterior Predictive p-value

Bayesian posterior predictive $p$-value is meant to estimate how likely we are
to observe the data described by our postfit model if we were to take the same
amount of data again. Therefore, it is a much more demanding $p$-value test than
the frequentist $p$-value, which uses the larger prior parameter phase space.

Firstly, an ensemble of parameter values explored by the MCMC, once the
stationary state has been reached, is used. We draw parameter values from a
random MCMC step after the _burn-in_ stage and build the predictions for each
sample (by reweighting the nominal MC to the drawn parameter values). Then, we
statistically fluctuate the drawn prediction by applying Poissonian smearing to
each bin. Afterwards, for each sample, we calculate -2LLH between the drawn
prediction and its statistical fluctuation: _-LLH(Draw Fluc, Draw)_, and
similarly between the drawn prediction and the data distribution:
_-LLH(Data, Draw)_. We repeat this process a few thousand times. An example of
_-LLH(Data, Draw)_ vs. _-2LLH(Draw Fluc, Draw)_ is shown below.

<img width="60%" alt="image" src="https://github.com/user-attachments/assets/519d4b46-5d11-402a-858b-9e9fc9daf99e" />

We identify two methods for calculating the $p$-value, statistically
fluctuating two different distributions. The first method uses the prediction
from the draw _-LLH(Draw Fluc, Draw)_, and the other uses the averaged
prediction for all draws and its statistical fluctuation
_-LLH(Pred Fluc, Draw)_. On average, we expect the $p$-value from the second
method to be better.

The p-value is the ratio of number of draws below the y = x line to all considered draws.

## References

[1] Kamil Skwarczynski PhD thesis.
