# Variable Frequency Oscillation

An equation for varying the frequency of an oscillating function over time, and a Maya expression that implements it.

## The Function

Let's say we have a function $f(t)$ that we're using to animate the position of an object over time. If we wanted to make the object bounce up and down, we could model that using $f(t) = sin(\omega t)$, where $t$ is the current time and $\omega$ is the angular frequency (which defines how fast the object oscillates):

![alt text](assets/SimpleSine_ManimCE_v0.18.0.gif)

This works fine when $\omega$ is constant, but what if we want to make the object speed up and slow down as it wiggles? Instead of a constant $\omega$, we would need a function $\omega (t)$ that defines what the angular frequency should be at a given time:

![alt text](assets/MysteryFunction_ManimCE_v0.18.0.gif)

Now we have a new question: how should we define $f(t)$? The first thing we could try is plugging $\omega (t)$ into the equation we had before, which would give us $f(t) = sin(\omega (t) \cdot t)$. However, doing so gives us some unwanted behavior:

![alt text](assets/BadFunction_ManimCE_v0.18.0.gif)

When the value of $\omega (t)$ is constant, $f(t)$ behaves the way we want it to. But as soon as $\omega (t)$ starts changing, $f(t)$ starts oscillating much faster than it should for the current $\omega$ value. Then it abruptly slows down once $\omega$ becomes constant again. To understand why this happens, we can look at how $\omega(t) \cdot t$ changes over time:

![alt text](assets/BadFunctionExplanation_ManimCE_v0.18.0.gif)

When $\omega (t)$ is constant, $\omega(t) \cdot t$ increases linearly with $t$. But once $\omega (t)$ starts increasing too, it multiplies with the already increasing $t$ to create a signficiant jump in the overall rate of change of $\omega(t)\cdot t$. The function $f(t) = sin(\omega t)$ is only able to model this sort of motion when $\omega$ is constant. In order to vary $\omega$ over time, we're going to need to find a different function.

In order to do this, it can be helpful to think more closely about the effect that $\omega$ has on $f(t)$. One way to think about $\omega$ is that it controls the "stretchiness" of the function. Lower $\omega$ values expand it, resulting in slower oscillation, and higher $\omega$ values compress it, resulting in faster oscillation:

![alt text](assets/ExpandContract_ManimCE_v0.18.0.gif)

However, we can also think of $\omega$ as setting the speed we travel along the horizontal axis when evaluating $f(t)$. Instead of increasing our oscillation speed by compressing the curve and moving along the horizontal axis at a constant rate, we can increase our oscillation speed by keeping $f(t)$ the same but changing the rate at which we traverse it. The graph of $f(t)$ is represented differently, but the final outcome for the oscillating object is the same:

![alt text](assets/SpeedVariation_ManimCE_v0.18.0.gif)

This way of thinking about $\omega$ is a bit more convoluted than the stretchiness model, but it creates an interesting property: we are now thinking of $\omega$ as a velocity, which means we can integrate it to get a position. 

If $\omega (t)$ represents the rate at which we're travelling along the horizontal axis, then $\int_{0}^t \omega (t) \, dt$ represents the current horizontal position at time $t$. That essentially means that $\int_{0}^t \omega (t) \, dt$ is an expression that tells us what number to plug in to our oscillating function in order to model a changing $\omega$. In other words, it's our solution:

$$ f(t) =sin(\int_{0}^t \omega (t) \, dt) $$

Now we can revisit our examples from before with our new definition for $f(t)$. If we look at how $\int_{0}^t \omega (t) \, dt$ changes over time, we see a smooth transition instead of the sharp one that $\omega (t) \cdot t$ yielded:

![alt text](assets/GoodFunctionExplanationLabeled_ManimCE_v0.18.0.gif)

And when we apply this animation to our oscillating object, we get the desired result:

![alt text](assets/MysteryFunctionLabeled_ManimCE_v0.18.0.gif)

As an additional way to check our work, we can look at how our new function reacts if $\omega(t)$ is constant. Lets set $\omega(t)$ to a constant function:
$$ \omega(t) = \omega_1 $$
Then $\int_{0}^t \omega (t) \, dt$ evaluates as follows:
$$\int_{0}^t \omega (t) \, dt = \int_{0}^t \omega_1 \, dt = \omega_1t$$
So we end up with:
$$f(t) =sin(\int_{0}^t \omega (t) \, dt) = sin(\omega_1t)$$
Which is the same function that we started with when $\omega$ was constant. This makes $f(t)=sin(\omega t)$ a special case of the more general function $ f(t) =sin(\int_{0}^t \omega (t) \, dt) $.

## Applications

While I used $sin$ as an example, this general process applies to any function that animates over time. For any continuous function $g(t)$, an integrable function $\omega(t)$ can be used to change the rate at which $g(t)$ is traversed:

$$ f(t) =g(\int_{0}^t \omega (t) \, dt) $$

Here's an example using a noise function:

![alt text](assets/NoiseFunctionLabeled_ManimCE_v0.18.0.gif)

Another interesting property of this method is that negative $\omega$ values will reverse the traversal direction of $g(t)$, which can be used to create symmetry: