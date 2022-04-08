#!/usr/bin/env python3
import re
import logging

from urllib import parse
from re import Pattern
from argparse import ArgumentParser

import requests


# DOI pattern
DOI_PAT = re.compile(r"\[ *?10.*? *?\]")
BIB_ITEM_PAT = re.compile(r"\b(?P<key>\w+)={(?P<value>[^}]+)}")
BIB_TYPE_PAT = re.compile(r"@(\w+)")
FIRST_WORD = re.compile(r"\w+")

def test_func():
    article = "@article{2004, title={Finishing the euchromatic sequence of the human genome}, volume={431}, ISSN={1476-4687}, url={http://dx.doi.org/10.1038/nature03001}, DOI={10.1038/nature03001}, number={7011}, journal={Nature}, publisher={Springer Science and Business Media LLC}, year={2004}, month={Oct}, pages={931â\x80\x93945}}"
    bib_pat = re.compile(r"\b(?P<key>\w+)={(?P<value>[^}]+)}")
    bib_pat.findall(article)
    re.findall(r"@(\w+)", "@article{title={this is a title}}")[0]


# Logging
def logman(name: str = "pr_logger", level: int = logging.DEBUG):
    logger = logging.Logger(name=name)
    stream_hand = logging.StreamHandler()
    stream_hand.setLevel(level)

    log_fmt = logging.Formatter("{levelname: >8}|{asctime: >18}| {message}",
                                style="{", datefmt="%y-%m-%d,%H:%M:%S")
    stream_hand.setFormatter(log_fmt)

    logger.addHandler(stream_hand)
    
    return logger


def cli_opts():
    """Get CLI options."""
    parser = ArgumentParser(description="A CLI tool to make bibtex from DOIs.")

    parser.add_argument(
        "-t", "--in-tex-file", required=True, metavar="FILE",
        help="The TEX file from which obtain the DOI.")
    parser.add_argument(
        "-c", "--cite-mthd", default="cite", choices=["cite", "citep"],
        help="The command used to cite a paper. Default: %(default)s")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="Verbose level, count variable.")
    parser.add_argument(
        "-o", "--out-tex-file", default="output.tex", metavar="FILE",
        help="The output file whose DOIs were translated to a bibtex key.")
    parser.add_argument(
        "-O", "--out-bib-db", default="output.bib", metavar="FILE",
        help="The output bib database including the bib record fetched for"
        " each DOI in the input TEX file. Default: %(default)s")
    parser.add_argument(
        "--out-modes", default="w,a", metavar="CHAR,CHAR",
        help="The mode for the output file. Default: %(default)s")

    return parser


def fetch_bib_by_doi(doi: str,
                     logger: logging.Logger,
                     base_url: str = "https://doi.org", # A redirection will be done by the crossref
                     style: str = "bibtex"):
    """Fetch bibtex record from the given database."""

    headers = { "Accept": f"text/bibliography; style={style}" }

    with requests.Session() as session:
        doi_list = doi.strip("[").strip("]").replace(" ", "").split(";")

        for per_doi in doi_list:
            if not per_doi:
                logger.warning(f"Bad DOI: {per_doi}")
                continue

            
            doi_url = parse.urljoin(base_url, per_doi.replace("\\", ""))
            response = session.post(doi_url, headers=headers)

            # Ensure the encoding is utf-8 (http://docs.python-requests.org/en/master/user/quickstart/#response-content)
            response.encoding = "utf-8"

            text = response.text.strip()

            if not text:
                logger.error(f"Nothing for [{per_doi}], please check it manually.")

            bib = dict(BIB_ITEM_PAT.findall(text))

            # Preapre the entry key AuthorYearTitle
            author_matches = FIRST_WORD.findall(bib.get("author", "Author"))
            author = author_matches[0] if author_matches else "Author"

            title_matches = FIRST_WORD.findall(bib.get("title", "Title"))
            title = title_matches[0] if title_matches else "Title"

            year = bib.get("year", "")

            bib_entry = f"{author}{year}{title}"

            if author == "Author" or title == "Title" or year == "":
                logger.debug(text)
                logger.debug(bib)

            # BIB type, article, book etc.
            bib_type_matches = BIB_TYPE_PAT.findall(text)
            bib_type = bib_type_matches[0] if bib_type_matches else "article"

            # The BIB body.
            bib_body = ", ".join([f"{k}={{{v}}}" for k, v in bib.items()])

            # The updated record
            bib_rec = f"@{bib_type}{{{bib_entry}, {bib_body}}}\n"

            logger.debug(f"{bib_type}, {bib_entry}, {per_doi}")

            yield [per_doi, bib_entry, bib_rec]


def fetch_doi_from_tex(tex_line: str, doi_pat: Pattern):
    if tex_line.strip()[:1] in ["", "%"]:
        # logger.debug(f"{tex_line.strip()}")
        return False, tex_line

    pat_match = doi_pat.findall(tex_line)
    if pat_match:
        return True, pat_match

    return False, "<Empty>"


def main():
    # CLI options
    parser = cli_opts()
    opts = parser.parse_args()

    in_tex_file = opts.in_tex_file
    cite_mthd = opts.cite_mthd
    verbose = opts.verbose
    out_tex_file = opts.out_tex_file
    out_bib_db = opts.out_bib_db
    out_modes = opts.out_modes

    out_tex_mode, out_bib_mode = out_modes.split(",")

    # Logging
    log_name = "pr_logger"
    log_level = max(10, 40 - verbose * 10)
    logger = logman(log_name, log_level)

    with open(in_tex_file, "r") as in_tex_hdl, \
            open(out_tex_file, mode=out_tex_mode) as out_tex_hdl, \
            open(out_bib_db, mode=out_bib_mode) as out_bib_hdl:
        exist_entries = []

        for p_line in in_tex_hdl:
            has_doi, doi_unit = fetch_doi_from_tex(p_line, DOI_PAT)

            if has_doi:
                for p_unit in doi_unit:
                    all_entry = []
                    bib_rec = fetch_bib_by_doi(p_unit, logger)
                    for (p_doi, per_entry, per_rec) in bib_rec:
                        all_entry.append(per_entry)

                        if per_entry not in exist_entries:
                            exist_entries.append(per_entry)
                            out_bib_hdl.write(per_rec)
                        else:
                            logger.warning(
                                f"{per_entry} exists in {out_bib_db}, skip.")

                        assert p_doi in p_unit, f"No {p_doi} in {p_unit}"

                    bib_entry = ",".join(all_entry)
                    cite_str = f"\\{cite_mthd}{{{bib_entry}}}"

                    p_line = p_line.replace(p_unit, cite_str)

            out_tex_hdl.write(p_line)
    logger.warning("Please use diff to check the replaced citations.")


if __name__ == "__main__":
    main()
