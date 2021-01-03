## Dual Timer
Dual Timer is a GUI with keyboard input that allows a user 
to simultaneously record two interaction types and their 
duration over a set period of time.

<p align="center">
  <img src="/assets/DualTimer.gif" width="400"></img>
</p>

## Motivation
A common test for learning and memory in mice is the
[Novel Object Recognition (NOR) task](https://med.stanford.edu/sbfnl/services/bm/lm/bml-novel.html)
where the time spent exploring a novel object vs a familiar object
is compared. Mice naturally spend more time exploring novel objects, but
if memory or recognition is impaired, they will spend equal time exploring both objects.

To record the duration of exploration with both objects, researchers have to use two separate timers. This can be 
cumbersome and leads to measurement errors. I wanted to make a simple tool that made it easier for researchers
to record their data.

## Features
- Keyboard input: 
    - Timer 1 - a 
    - Timer 2 - d 
    - Pause - space
- Exports data as a CSV (duration of each interaction)
<p align="center">
    <img src="/assets/Output.png" height="300"></img>
</p>

## Built using
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for GUI and keyboard input 
