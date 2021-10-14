# Zhenhua Zhang's Ph.D. thesis 2021

## Link expression to genetic architecture

This is the repository for my Ph.D. thesis and it will be publicly available on
xx-xx-2021.

## Files and directories
```
├── figures/
│   ├── cover.jpg
│   └── README
├── misc/
├── src/
│   ├── timeline.tex
│   ├── zzhang_phd_thesis.bib
│   ├── zzhang_phd_thesis.cls
│   └── zzhang_phd_thesis.tex
├── LICENSE
├── Makefile
└── README.md
```


## Build

The thesis was prepared using TeX Live (2020) on Debian 10 distribution. To
compile, a `Makefile` is available along with the repository to compile
`src/*.tex` files into one `pdfs/phd_thesis_zzhang.pdf` file for the whole
thesis.

Hence, the thesis can be compiled by one line command under shells, e.g., `zsh`
on Linux distribution like Debian/Ubuntu.

``` {bash}
cd phd_thesis_zzhang/
make
```

Also, for the convinience to revise it in Office suit like MS Office, the
`.tex` can be compiled into `.docx` by:

``` {bash}
make name-of-file.docx
```

To clean up the intermediate files during preparation of `.pdf`, use:

``` {bash}
make clean    # remove all intermediate and `.pdf` files
make clean-build  # remove the intermediate files
```

## Contact

For more information, please contact zhenhua.zhang217@gmail.com

## License

Attribution 4.0 International (CC BY 4.0). For more information, check LICENSE.

<!-- vim: set ai ft=pandoc ts=4 tw=120: -->
