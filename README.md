# GWBar

A gravitational-wave progressbar template for LaTeX beamer presentations.

## Usage

To import and activate the template, run

```latex
\usepackage{gwbar}
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
hase some GWPy ``TimeSeries`` on hand, this preparation can be done using
`signal_export` function in the accompanying python script.

***Note:*** in case the bar looks misaligned in some compiler like Overleaf,
this will typically disappear in the exported pdf. I do not know why this
happens, but I have experienced it several times.

## Examples

To see how this beamertemplate looks like and how it can be used, have
a look at the `examples` folder in this repository.

## Plans

- allow for adjustable height and width of the signal

If you have any ideas or suggestions, please feel free to tell me about them!
