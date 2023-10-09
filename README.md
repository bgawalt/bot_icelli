# bot_icelli

Your typical digital image is perfectly represented as a *pixel table* with five
integer-valued columns, with one row per pixel in the image:

1.  The row index of the pixel,
2.  The column index of the pixel,
3.  How red is the pixel, on a scale from 0 to 255,
4.  How green is it, and
5.  How blue is it.

It takes a lot space and time to write down all five of those numbers, for every
pixel in the image, and so we all agree it's a good idea to use compressed
representations of digital images.

This project, Bot_icelli, is dedicated to taking one *specific* image, with its
five-column table of pixel data, and treating it like a regression problem:

*  **Model inputs:** two dimensional: pixel row; pixel column
*  **Model outputs:** three dimensional: redness, greenness, blueness

Using whatever modeling techniques are cheap and handy, Bot_icelli overfits a
model to a specific image's pixel table.

(Note: there's no transfer from some larger body of images, to the model fit for
the one specific image.  Every model starts totally ignorant of what a "typical"
image "usually" looks like. Every model gets their own specific pixel table, and
that's it.  I leave the "learn a lossy image representation that works well in
general" work to the Joint Photographic Experts Group, &c.)

ML models are function approximators, "glorified curve fitting" in Judea Pearl's
words.  So let's fit a weird curve that *mostly* follows your specific image's
`(row, col) -> (R, G, B)` function.

## Usage

First, set up your Python environment with the two dependencies:

```
$ pip install imageio
$ pip install -U scikit-learn
```

## Roadmap

This is destined to become a Bluesky bot who applies familiar models --
e.g., "a boosted forest of 50 trees, each of depth 2" -- to the profile pictures
of those who follow it. Everyone gets a neat little filter applied to their
avatars that you can't find in Photoshop.

TODO:

1.  Get demo output from a single decision tree running again.
2.  Write the "fetch a Bluesky follower's profile picture" routine.
3.  Set up the "cache images locally, in, like, SQLite" routine.
4.  Learn to post images to Bluesky.