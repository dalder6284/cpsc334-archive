# Stained

In the middle of class last week, the idea came to me that I wanted to do something with two-point perspective. If I have a horizon line with two vanishing points, I can draw things framed on that perspective so that they look three-dimensional.

![image.png](/project-1/images/two-point-example.png)

It starts with math. I had two vanishing points on each edge of the screen. I pick two other vertices that form a vertical line down the middle of the screen. Finally, the other two vertices of the quadrilateral are determined by a vector that is determined by the two vanishing points and the original vertical line points.

My first try was interesting. See below.

![image.png](/project-1/images/first-iteration.png)

Very quickly you can kind of see some sort of dimension jump out at you. They seem to be following some kind of curve that’s skewed to the right, but I believed that the two-point perspective should be rather centered on average. It *looks* 3D, but it doesn’t feel like two-point perspective. It looks rather orthogonal. Like I’m playing *The Sims*.

It turned out I was miscalculating the vectors towards the horizon points. Now, it was starting to look more like what I wanted.

![image.png](/project-1/images/second-iteration.png)

Since it was just laying quads over quads in this trippy perspective, they looked like bricks being laid in front of each other. It was like a building was being built towards you endlessly.

![ezgif-5-c3af498c3a.gif](/project-1/images/second-iteration-animation.gif)

It looked good and I was getting happy with it. In this iteration, it looks like panes of colored glass put together, but when I removed the border…

![image.png](/project-1/images/watercolor.png)


It looked more like strokes of paint? And I liked that more, so I kept it. I started messing around with the opacity and the padding of the scene, too. 

![image.png](/project-1/images/full-watercolor.png)

As the animation goes on, you start to see levels, almost like the corner of a street. Certain pieces look like windows or doors on other pieces. It feels a bit cramped, but if I try, it looks really open at the same time, a little bit like the floor of a warehouse or parking lot. In case you were wondering what the previous iteration looks like with this paint aesthetic…

![image.png](/project-1/images/weird-watercolor.png)

I like it, but not as much as its brother. Don’t tell it I said that. It does give a more brushy feeling as it progresses, however, which is nice if you like that, but there’s no form.

### Timing

The timing was pretty simple. I initially started with a random time from some small value to a larger value (50 ms to 1 second, for example). However, that felt a little boring, so I skewed it using a power function. It gives a bit more of a rain pattern, or like paint being splattered on a page. There’s small bursts of drawing with a gap every once in a while.

```jsx
int skewedTime(int minTime, int maxTime) {
  float v = pow(random(1), 4);
  int delay = int(map(v, 0, 1, minTime, maxTime));
  return delay;
}
```

### Color Palette

Testing started out with just a random color calculated like so:

```jsx
  color c = (color) random(#000000);
```

In order to get better colors, what should I do? I looked at a bunch of algorithms for it, but none of them looked good, really. So, I just downloaded a few famous paintings and chose a random pixel each time for the color of the next quad. I chose a random painting each time the application started.

Here’s *The Starry Night.*

![image.png](/project-1/images/starry-night.png)

An untitled piece by Keith Haring

![image.png](/project-1/images/keith-haring.png)

This is *The Great Wave off Kanagawa.*

![image.png](/project-1/images/great-wave.png)

### Running the Script

In order to run this program, you should have:

- A Raspberry Pi. I believe mine has 4 GB of RAM so anything of or above should work fine.
- Processing v.4. The Raspberry Pi has `aarch64`, so you should make sure to install the correct version for the correct platform. There is a separate download link for the Pi vs. some other Linux download. Unpack this `.tar.gz` file you receive. This folder should contain the compiler for the included `.pde` file.

In `~/.config/wayfire.ini`, you should add the following code (or append to `autostart` if the header already exists).
```
[autostart]
prcss = /path/to/shellscript/prcs.sh
```

The `prcs.sh` should be executable and contain the following:

```sh
/path/to/processing/processing-java --sketch=/path/to/sketch/folder --run
```

It should run on start up now, or if you just want to run it immediately, you could run the Processing IDE and run it from there or just run the bash script from the terminal.

As for the picking colors from the filename, you should try changing the filename to the directory where you have stored the photos. I have them here for convenience, but right now, they don't run out of the box. Give it a try. Use your own photos, too!

