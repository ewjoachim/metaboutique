import dataclasses
import datetime
import pathlib
import shutil
import subprocess

import htpy as h


@dataclasses.dataclass
class Post:
    html_safe: str
    link: str
    avatar_url: str
    preview_image_url: str
    mention_handle: str
    mention_name: str
    self_url: str
    datetime: datetime.datetime
    title: str


def build():
    page = str(build_page())
    build_folder = pathlib.Path("_build")

    shutil.rmtree(build_folder)
    build_folder.mkdir(parents=True)

    (build_folder / "index.html").write_text(page)
    shutil.copytree(pathlib.Path("static"), build_folder, dirs_exist_ok=True)
    subprocess.check_call(
        [
            "./tailwindcss",
            "--input=../style.css",
            "--output=style.css",
            "--optimize",
            "--cwd=_build",
        ]
    )


def build_page():
    title = "La Méta-boutique - Les bons conseils de Tatie Sandrine"
    tweet = Post(
        html_safe="",
        link="",
        avatar_url="",
        preview_image_url="",
        mention_handle="",
        mention_name="",
        self_url="",
        datetime=datetime.datetime.now(),
        title="",
    )
    return h.html[
        h.head[
            h.meta(charset="utf-8"),
            h.meta(http_equiv="X-UA-Compatible", content="IE=edge"),
            h.meta(name="viewport", content="width=device-width, initial-scale=1"),
            h.title[title],
            h.link(rel="stylesheet", href="main.css"),
            h.meta(name="language", content="fr-FR"),
            h.meta(name="robots", content="all"),
            h.meta(name="description", content=title),
            h.meta(
                name="keywords",
                content="boutique,créateurs,garagedeloffre,sandrine2loffre,liens,twitter,thread",
            ),
            h.meta(name="twitter:card", content="summary_large_image"),
            h.meta(name="twitter:site", content="@sandrine2loffre"),
            h.meta(name="twitter:creator", content="@sandrine2loffre"),
            h.meta(name="twitter:title", content=title),
            h.meta(
                name="twitter:description",
                content="La Méta-boutique recense des liens vers les boutiques de créatrices et de créateurs",
            ),
            h.meta(
                name="twitter:image",
                content="https://lametaboutique.fr/previewcard.jpg",
            ),
            h.meta(
                name="twitter:image:alt", content="Les bons conseils de Tatie Sandrine"
            ),
        ],
        h.body[
            h.section[h.div[h.div[h.figure[h.img(src="header.jpg", alt=title)]]]],
            h.section[
                h.div[
                    " {% for line in data|batch(3) %}",
                    h.div[
                        " {% for tweet in line %}",
                        h.div[
                            h.div[
                                h.div[
                                    h.a(
                                        href=tweet.link,
                                        title="Lien vers la boutique",
                                        style=f"background-image: url(_assets/{tweet.preview_image_url})",
                                        target="_blank",
                                    )
                                ],
                                h.div[
                                    h.div[
                                        " {% if tweet.mention_handle %}",
                                        h.div[
                                            h.a(
                                                href=f"https://twitter.com/{tweet.mention_handle}",
                                                target="_blank",
                                            )[
                                                h.figure[
                                                    h.img(
                                                        src=f"_assets/{tweet.avatar_url}",
                                                        alt=f"Image de profil de {tweet.mention_name}",
                                                    )
                                                ]
                                            ]
                                        ],
                                        h.div[
                                            h.a(
                                                href=f"https://twitter.com/{tweet.mention_handle}",
                                                target="_blank",
                                            )[
                                                h.p[f"{tweet.mention_name}"],
                                                h.p[f" @{tweet.mention_handle}"],
                                            ]
                                        ],
                                        """ {% else %}
                    {% if tweet.title %}""",
                                        h.p[
                                            h.a(href=tweet.link, target="_blank")[
                                                f" {tweet.title}"
                                            ]
                                        ],
                                        """ {% endif %}
                    {% endif %}""",
                                    ],
                                    h.div[
                                        tweet.html_safe,
                                        h.br,
                                        h.a(
                                            href=tweet.self_url,
                                            target="_blank",
                                        )[
                                            h.time(datetime=tweet.datetime.isoformat())[
                                                f"{tweet.datetime:%Y-%m-%d %H:%M}"
                                            ]
                                        ],
                                    ],
                                ],
                            ]
                        ],
                        " {% endfor %}",
                    ],
                    " {% endfor %}",
                ]
            ],
            h.footer[
                h.div[
                    h.div[
                        h.div[
                            h.p[
                                h.strong[" La Méta-boutique"],
                                " est un site généré automagiquement à partir des tweets de",
                                h.a(
                                    href="https://twitter.com/sandrine2loffre/status/1277912722638876672"
                                )["ce fil de Sandrine Deloffre"],
                            ],
                            h.small[
                                h.p[
                                    " Conception: ",
                                    h.a(href="https://twitter.com/ewjoachim")[
                                        "Joachim Jablon"
                                    ],
                                    " | Le code du site est en ",
                                    h.a(
                                        href="https://github.com/ewjoachim/metaboutique"
                                    )["Open Source"],
                                    " sous ",
                                    h.a(
                                        href="https://github.com/ewjoachim/metaboutique/blob/master/LICENSE"
                                    )["licence MIT"],
                                    ".",
                                    h.br,
                                    " Les avatars et vignettes sont la propriété de leurs auteur·ices respectif·ves.",
                                    h.br,
                                    " Les illustrations du site sont signées par l'adorable Sandrine Deloffre, bien sûr.",
                                ],
                                h.p[
                                    " Si vous souhaitez modifier ou supprimer une carte vous concernant, contactez",
                                    h.a(href="https://twitter.com/ewjoachim")[
                                        "Joachim"
                                    ],
                                    " ou ouvrez un",
                                    h.a(
                                        href="https://github.com/ewjoachim/metaboutique/issues/new"
                                    )["ticket GitHub"],
                                    ".",
                                ],
                            ],
                        ]
                    ],
                    h.div[
                        h.figure[
                            h.img(
                                src="couillard.png",
                                title="Un embelissement typographique, comme par exemple un astérisme (3 astérisques ensemble) qui sépare ou clôture un paragraphe, ça s'appelle un couillard. Je ne sais pas ce que je dois faire de cette information. Votez #Flibuste2027",
                            )
                        ]
                    ],
                ]
            ],
        ],
    ]
