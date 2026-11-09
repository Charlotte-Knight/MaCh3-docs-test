# Splines

## What is a spline?

MaCh3's {cpp:class}`SplineBase` interface is implemented by classes such as
{cpp:class}`BinnedSplineHandler`.
Spline, sometimes called response function, encodes dependence between parameter value and weight.
By having these complex responses precomputed, it allows evaluating weight during fit time very fast.

We usually store several points at which weight were evaluated, called knots.
Thus, we need to interpolate between points interpolation type is up to user
as MaCh3 has several options available.

## Spline Interpolation (3-rd order polynomials)
Default interpolation is kTSpline3. It follows ROOT TSpline3 implementation.

<img width="350" src="https://github.com/user-attachments/assets/4e32f8b9-c024-4563-85c0-bce9b3e34fa7">

Above is the most common example of response function/spline for which all available options perform similarly.

However, there are examples where we want to enforce linear interpolation as this is the desired response.
Usually in situation when we reweight between different models. For this, recommended is kLinear.

<img width="350" src="https://github.com/user-attachments/assets/bc92e99d-ee41-4ae3-9b55-61ec5cdb3d0e" />

<img width="350" src="https://github.com/user-attachments/assets/0248e6c8-1a01-424a-b1cf-7061fd275bd2" />

Another often encountered case is where there are large differences between weight, resulting in so called ringing:

<img width="350" src="https://github.com/user-attachments/assets/b91e6194-870c-4255-b12d-f2dc20c455d3" />

For such case-based options are kMonotonic which ensures spline segments are monotonic or kKochanekBartels.

## Linear Function
Since quite often we are using linear responses, it is generally recommended to reduce number of splines knots.
As more spline knots doesn't contribute to better response, but each knot affects RAM.

<img width="350" src="https://github.com/user-attachments/assets/774dd6c2-7826-481b-a81b-9ce8569052cd" />

Another option is to use kLinearFunc which simple performs linear function (a*x+b) resulting in much better performance
and less RAM.

<img width="350" src="https://github.com/user-attachments/assets/571c5d43-9026-46cb-9621-2e68142f8e5f" />

## Spline Extrapolation
For extrapolating beyond the limits of the spline we calculate the weight using the closest segment. This is essentially 'extending' the first segment below the first knot if extrapolating below the spline limits, or extending the last segment above the last knot if extrapolating above the limits. With linear function this simply uses the same coefficients as used for the rest of the spline.

### GPU
Since the calculation of event by event spline is quite often the bottleneck, there is GPU support for these calculations. From developer and user point of view, code works the same. If GPU support is enabled, MaCh3 will copy spline information to the GPU and perform calculations there.

<img width="600" src="https://github.com/mach3-software/MaCh3/assets/45295406/34f7aeaf-d40e-4e8c-96f7-a1eb197603ea" />
