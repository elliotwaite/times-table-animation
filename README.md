## Times Table Animation Script

The code in this repository ([generate_frames.py](generate_frames.py)) can be used to generate times table animations like the following:

https://www.youtube.com/watch?v=lm4s_3ixBn4

[<img src="https://img.youtube.com/vi/lm4s_3ixBn4/hqdefault.jpg">](https://www.youtube.com/watch?v=lm4s_3ixBn4)

This project was inspired by Mathologer's video, "Times Tables, Mandelbrot and the Heart of Mathematics": 

https://www.youtube.com/watch?v=qhbuKbxJsk8

[<img src="https://img.youtube.com/vi/qhbuKbxJsk8/hqdefault.jpg">](https://www.youtube.com/watch?v=qhbuKbxJsk8)


## Explanation

First, you pick a number for how many lines you want to display on each frame. I
picked 512 for the animation above because I thought it looked nice.
Given that I picked 512, you then make a circle with 512 equally spaced
points around it, which represent the values 0 to 511. You then multiply
each of those values (0 - 511) by a number (for example 2) to get the
place where that number maps to (1 maps to 2, 2 maps to 4, 3 maps to 6,
and so on). If you then connect those dots on the circle with a line
(connecting point 1 to point 2, and point 2 to point 4, and so on), you
get one of the patterns shown in the animation. If a value is mapped to
a number greater than or equal to 512, that value is divided by 512 and
the remainder value is used instead (this is also called applying a
modulo of 512). The multiple values can also be non-integers, for
example, if the multiple was 1.5, then the point at position 3 would get
connected to the point at position 4.5, which would just be the point on
the circle in between 4 and 5. Each frame is for a different multiple,
starting with a multiple of 1 and increasing it by a small amount (for
example 0.01) until the multiple is 513, which ends up producing the
same pattern as 1 does due to the fact that 513 mod 512 equals 1. I also
extend the line connecting the points beyond the edge of the circle to
the edge of the screen, so if a point would map back to itself (for
example the 0 point always maps back to itself, or when the multiple is
1, all points get mapped back themselves), then the line is just tangent
to the circle. I also colored the lines according to where the initial
point is on the circle, just using the sequence of fully saturated RGB
colors that cycle through the hues.


## License

[MIT](LICENSE)