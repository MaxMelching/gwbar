# GWBar

A gravitational-wave progressbar template for LaTeX beamer presentations.

## Usage

To import and activate the template, run

```latex
\usepackage[options]{gwbar}
\setbeamertemplate{frametitle}[gwbar]
```

For this to work, the `.sty` and `.txt` files in this repository have to
be either in the same directory as the corresponding LaTeX file or they
have to be in a directory where your LaTeX distribution finds them. The
location of the `.txt` can also be given as an argument to the package
(called `templatefile`).

It is possible to use any waveform you want in the presentation. The only
requirement for the displaying to work properly is that the values are
between $-1$ and $+1$, and that the times are between $0$ and $1$. If you
have some GWPy ``TimeSeries`` on hand, this preparation can be done using
`signal_export` function in the accompanying python script.

***Note:*** in case the bar looks misaligned in some compiler like Overleaf,
this will typically disappear in the exported pdf. I do not know why this
happens, but I have experienced it several times. You can confirm that
everything is calculated correctly by zooming in on the transitions.

### Arguments

Inplace of a separate documentation pdf, the few existing options for the
package will be discussed here:

- `templatefile`: the file used for plotting. Must adhere the TikZ requirements
  on the `plot file` function: two colums of equal length, with the first one
  representing x-data and second one representing y-data. As mentioned in the
  text, for proper displaying there are constraints on the values in this file.

- `leftpadding`: starting point of signal on the frame, i.e. spacing between
  left end of the frame and beginning of the signal (which coincides with
  the point where the progressbar starts). Default is `0.6\textwidth`.

- `rightpadding`: end point of signal on the frame, i.e. spacing between
  right end of the frame and end of the signal. Default is `0.1\paperwidth`.

- `signalheight`: height of the plotted signal. By default, the signal will be
  plotted so that it touches the upper end of the frame (the corresponding
  option value is `"frametitleheight"`). To have the signal touch the lower end
  of the framesubtitle (which will usually be crossed for the default setting),
  `"framesubtitleheight"` can be given. It is also possible to pass any other
  length for a fixed, custom height. Note that the two strings mentioned here
  should be the most robust options, as they calculate the length on each frame
  and thus are able to react to things like changes in font size.
  
  To adjust the height manually in between frames, pass a length variable to
  `signalheight` and change the value of this variable accordingly (cf. the
  `examples/signalheight_example` file).

- `signalupshift`: controls how much separation is between the lower end of the
  frametitle part (upper end of framesubtitle) and the progressbar. Default is
  3pt, so that the progressbar does not intersect with the framesubtitle.

- `bottompaddingnosubtitle`, `bottompaddingwithsubtitle`: padding applied after
  the template. This requires two options because it might be desirable to apply
  different paddings for frames with/without subtitle. The reason to allow for
  padding at all is that the signal might overlap with the first text row
  otherwise, which is visually not very pleasing.

- Styling: albeit not being a direct option that can be passed, it is possible
  to change the progressbar style by editing the corresponding TikZ styles:
  
  ```tex
  \tikzset{<style name>/.style={<style options>}}
  ```

  (cf. the `examples/style_example` file). Styles used by the template are
  `gwbar@linelayerone`, `gwbar@linelayertwo`, `gwbar@fillinglayerone`, and
  `gwbar@fillinglayertwo`.

### Examples

To see how this beamertemplate looks like and how it can be used, have
a look at the `examples` folder in this repository.

## Plans

- Figure out a better syntax for bottompadding option

- Make the whole thing faster. Unfortunately, TikZ is inherently slow with
  plotting the potentially large number of points. Since we rely on a TikZ picture
  for every single frame, this can result in a rather slow compilation.

If you have any ideas or suggestions, please feel free to tell me about them!
