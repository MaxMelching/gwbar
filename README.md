# GWBar

A gravitational-wave headline and progressbar template for LaTeX files and
LaTeX beamer presentations.

## Usage

To import and activate the template in a "normal" LaTeX file, run e.g.

```latex
\usepackage[
    option=value,
    ...,
]{gwbar}
\ihead{\gwbar[option=value]{}Header Text}
```

(in files that use a KOMA-script documentclass). The `fancyhdr` package can be
used in a similar way. When testing this package, this turned out to be the
most versatile (and natural) way of providing the aspired functionality.

Similarly, to activate it in a beamer file, run e.g.

```latex
\usepackage[
    option=value,
    ...,
]{gwbar}
\setbeamertemplate{frametitle}[gwbar]
```

For either of them to work, the `.sty` and `.txt` files in this repository have
to be either in the same directory as the corresponding LaTeX file or in a
directory where your LaTeX distribution finds them. The location of the
`.txt` can also be given as an argument to the package (called `templatefile`).
For details on this, please have a look at the [Installation section](#installation).

It is possible to use any waveform you want in the presentation. The only
requirement for the displaying to work properly is that the values are
between $-1$ and $+1$, and that the times are between $0$ and $1$. If you
have some GWPy ``TimeSeries`` on hand, this preparation can be done using
`signal_export` function in the accompanying python script.

***Note:*** in case the bar looks misaligned in some compiler like Overleaf,
this will typically disappear in the exported pdf. I do not know why this
happens, but I have experienced it several times. You can confirm that
everything is calculated correctly by zooming in on the transitions.

## Installation

Unfortunately, adding LaTeX packages is not as easy as Python packages. I do not
claim to be an expert in this, but here are two ways I have found to make this work:

1. putting the relevant `.sty` files into the same directory as the `.tex` you
   plan to use them in. Then, `\usepackage{gwbar}` works. If your
   folder structure is slightly more complicated, a path like
   `\usepackage{../gwbar}` works too (despite some complaints by LaTeX).
   This is also the preferred way in case you are using Overleaf.

1. for a recipe on how to make the package available on your whole system,
   please refer to the instructions on
   [my GitHub](https://github.com/MaxMelching/latex_package_install).
   (Note that the location of the `.txt` can also be given as an argument to
   the package, called `templatefile`. Thus you only have to place the
   `gwbar.sty` file here.)

The `.txt` files must simply be in a location where you can find them, since
their path is expected as an argument. I could not find a way of dealing with
this using something like `TEXINPUTS`.

### Arguments

In place of a separate documentation pdf, the few existing options for the
package will be discussed here (apologies for my laziness):

- `templatefile`: the file used for plotting. Must adhere the TikZ requirements
  on the `plot file` function: two colums of equal length, with the first one
  representing x-data and second one representing y-data. As mentioned in the
  text, for proper displaying there are constraints on the values in this file.

  A value of `"none"` is used to encode that a flat line shall be drawn.

- `backgroundsignal`: a file that is plotted in the background of the
  `templatefile` and can thus represent underlying data (and, if the
  progressbar is activated, be "recovered" by it as part of the progressbar).

- `progressbar`: whether the package is used as a progressbar. Only has an
  effect in beamer files (it is forced to be disabled in other files), where
  it can be set to `true` (the default) or `false`.

- `leftpadding`: starting point of signal on the frame, i.e. spacing between
  left end of the frame and beginning of the signal (which coincides with
  the point where the progressbar starts). Default is `0.6\textwidth` in
  beamer files and `0.45\textwidth` otherwise.

- `rightpadding`: end point of signal on the frame, i.e. spacing between
  right end of the frame and end of the signal. Default is `0.1\paperwidth`
  in beamer files and `0.05\textwidth` otherwise.

- `signalheight`: height of the plotted signal(measured from zero, i.e. the total
  signal height is twice of this). Defaults to `\headheight` in non-beamer files.
  
  In beamer files, on the other hand, the signal will be plotted so that it
  touches the upper end of the frame (the corresponding option value is
  `"frametitleheight"`). To have the signal touch the lower end of the
  framesubtitle (which will usually be crossed for the default setting),
  `"framesubtitleheight"` can be given. It is also possible to pass any other
  length for a fixed, custom height. Note that the two strings mentioned here
  should be the most robust options, as they calculate the length on each frame
  and thus are able to react to things like changes in font size.
  
  To adjust the height manually in between frames, pass a length variable to
  `signalheight` and change the value of this variable accordingly (cf. the
  `signalheight_example` examples file).

- `signalupshift`: controls how much separation is between the lower end of the
  frametitle part (upper end of framesubtitle) and the progressbar. Default is
  `3pt`, so that the progressbar does not intersect with the framesubtitle.

- `headwidth`: total width of the line drawn (signal plus padding). In beamer
  files, you will probably not want to mess with this setting and stick to the
  default value of `\paperwidth`.
  
  In other files, it defaults to the LaTeX default of `\textwidth`, but might
  be changed manually and in that case, the package needs to know this.
  Unfortunately, I could not find a robust automatic way of getting this length
  (due to the many different possible classes and packages that could be used
  to control is), so it must be passed manually.

- `bottompaddingnosubtitle`, `bottompaddingwithsubtitle`: padding applied after
  the template. This requires two options because it might be desirable to apply
  different paddings for frames with/without subtitle. The reason to allow for
  padding at all is that the signal might overlap with the first text row
  otherwise, which is visually not very pleasing.

- `declaretitlebox`: determines whether or not the frametitle is replaced,
  meaning it only takes an effect in beamer files (it is forced to be
  disabled in other files). Among other things, this setting determines whether
  `signalheight="frametitle", "framesubtitle"` work, which is true by default
  in beamer files.
  
  In case `declaretitlebox=false`, there are several ways that the progressbar
  can still be used in beamer files. One can still employ the `\gwbar` command via

  ```latex
  \addtobeamertemplate{frametitle}{}{\gwbar}
  ```
  
  or, instead of operating on the frametitle, stick to

  ```latex
  \setbeamertemplate{headline}[gwbar]
  ```

  (though some subtleties might apply in both cases). Please refer to the
  `examples/headline_demo` and `examples/headline_demo_advanced` files
  for more details. One problem is that the headline is considered to be a part
  of the frame, while the frametitle is considered part of the content. This
  leads to the frametitle being put on top of headline, in other words: if you
  have some title template that has a certain color and try to draw the headline,
  this won't work. Alternatively, adding to the frametitle or other layers of
  the frame may be used thanks to the `\gwbar` command.

- Styling: albeit not being a direct option that can be passed, it is possible
  to change the progressbar style by editing the corresponding TikZ styles:
  
  ```tex
  \tikzset{<style name>/.style={<style options>}}
  ```

  (cf. the `style_example` files). Styles used by the template are
  `gwbar@linestyle`, `gwbar@bglinestyle`, and for beamer files also
  `gwbar@fillinglayer`.

*Note:* besides giving them to calls of the `gwbar` package or command, you
can also change options by using the `\UpdateGWBarOptions[option=value]` command.
However, be careful when inserting a new line between `[` and the first option,
this may yield an error because the new line is interpreted as a space. This
can be solved by adding a percent sign after the bracket opening, i.e. using `[%`
and then opening up a new line (the same applies to calls of `\gwbar[...]`).

### Examples

To see how this beamertemplate looks like and how it can be used, have
a look at the `examples` folder in this repository.

## Plans

- Figure out a better syntax for bottompadding option

- Make the whole thing faster. Unfortunately, TikZ is inherently slow with
  plotting the potentially large number of points. Since we rely on a TikZ picture
  for every single frame, this can result in a rather slow compilation.

If you have any ideas or suggestions, please feel free to tell me about them!
