# Maya Variable Frequency Oscillation

- ADD CONDA CONFIG

A MEL script that allows you to keyframe the frequency of an oscillating object.

### How It Works
Periodic functions are a common way of defining an animation procedurally in situations where you want to make an object move back and forth. They're often defined something like this (note that any periodic function could be used here, but $sin$ is the one I'm using for demonstration purposes): 

$$f(t) =  sin(\omega t)$$
Where $t$ is the current time, $A$ is amplitude, $\omega$ is the angular frequency (rate of oscillation), and $\phi$ is phase shift. 

PICTURE OF CONSTANT MOTION ALONG WITH GRAPH

However, a limitation of this function is that it requires $A$, $\omega$, and $\phi$ to be constant. If you try to vary $\omega$ over time in order to make an object oscillate faster or slower using this function, you will get undesired behavior. On the left is 

MESSED UP OSCILLATION

$$f(t) =  Asin(\omega (t) t + \phi)$$

$$f(t) =  Asin(\int_{0}^t \omega (t) \, dt + \phi)$$

$$\int_{0}^t \omega (t) \, dt = \omega t \text{ for constant } \omega$$

### Limitations
Since this script calculates the final output by summing up the frequencies at every 

## Installation / Use