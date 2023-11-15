import reflex as rx
from reflex import Component, Hstack, Box

class State(rx.State):
    """The app state."""

    pass

dots: dict = {
    "@keyframes dots": {
        "0%": {"background_position": "0 0"},
        "100%": {"background_position": "40px 40px"},
    },
    "animation": "dots 4s linear infinite alternate-reverse both",
}

wave: dict={
    "@keyframes wave": {
        "0%": {"transform": "rotate(45deg)"},
        "100%": {"transform": "rotate(-15deg)"},
    },
    "animation": "wave 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite alternate-reverse both",
}

css: dict = {
    "app": {
        "_dark": {
            "bg": "#15171b"
        },
    },
    "header": {
        'width': '100%',
        'height': '50px',
        'padding': [
            "0rem 1rem",
            "0rem 1rem",
            "0rem 1rem",
            "0rem 8rem",
            "0rem 8rem",
        ],
        "transition": "all 550ms ease",
    },
    "main": {
        "property": {
            "width": "100%",
            "height": "84vh",
            "padding": "15rem 0rem",
            "justify_content": "start",
        }
    },
    "footer": {
        "width": ["100%", "90%", "60%", "45%", "45%"],
        "height": "50px",
        "align_items": "center",
        "justify_content": "center",
    }
}
# header class

class Header:
    def __init__(self):
        self.header: rx.Hstack = rx.hstack(style=css.get('header'))
        self.email: rx.Hstack = rx.hstack(  # Corregir aquí
            rx.box(
                rx.icon(tag="email", _dark={'color': "rgba(255,255,255,0.5)"})),
            rx.box(rx.text("hola@airaldo.com", _dark={'color': "rgba(255,255,255,0.5)"})),
            align_items="center",
            justify_content="center"
        )
        self.theme: rx.Component = rx.color_mode_button(
            rx.color_mode_icon(),
            color_scheme="none",
            _light={'color': 'black'},
            _dark={'color': 'white'}
        )

    def compile_component(self) -> list:
        return[self.email, rx.spacer(), self.theme]

    def build(self) -> Hstack:
        self.header.children = self.compile_component()
        return self.header
    

# main content area
class Main:
    def __init__(self) -> None:
        self.box: rx.Box = rx.Box(width='100%')

        self.name: rx.Hstack = rx.hstack(
            rx.heading(
                """Hi - I'm Esteban Airaldo""",
                font_size=['2rem', '2.85rem', '4rem', '5rem', '5rem'],
                font_weight="900",
                _dark={
                    "background": "linear-gradient(to right, #e1e1e1, #757575)",
                    "background_clip": "text",
                }
            ),
            rx.heading(
                "👋🏼",
                size="2xl",
                style=wave,
            ),
            spacing="1.75rem",
        )

        self.badge_stack_max: rx.Hstack = rx.hstack(spacing="1rem")
        self.badge_stack_min: rx.Vstack = rx.vstack(spacing="1rem")
        titles= list = ["Entry Level Software Developer", "UI/UX Designer", "Python Developer Jr"]
        self.badge_stack_max.children = [self.create_badges(title) for title in titles]
        self.badge_stack_min.children = [self.create_badges(title) for title in titles]

        self.crumbs: rx.Breadcrumb = rx.breadcrumb()
        data: list = [
            ["/github.png", "GitHub", "#"],
            ["/youtube.png", "Youtube", "#"],
            ["/xcom.png", "Xcom", "#"],
        ]
        self.crumbs.children = [self.create_breadcrumb_item(path, title, url) for path, title, url in data ]
        


    # method: create social links
    def create_breadcrumb_item(self, path: str, title: str, url: str = None):
        return rx.breadcrumb_item(
            rx.hstack(
                rx.image(
                    src=path,
                    html_width="24px",
                    html_height="24px",
                    _dark= {"filter": "brightness(0) invert(1)"},
                ),
                rx.breadcrumb_link(
                    title,
                    href=url,
                    _dark={"color": "rgba(255,255,255, 0.7)"},
                )
            )
        )
        ...


    # method: create badges
    def create_badges(self, title: str) -> None:
        return rx.badge(
            title,
            variant="solid",
            padding=[
                "0.15rem 0.35rem",
                "0.15rem 0.35rem",
                "0.15rem 1rem",
                "0.15rem 1rem",
                "0.15rem 1rem",
            ],
        )

    def compile_desktop_component(self) -> Component:
        return rx.tablet_and_desktop(
            rx.vstack(
                self.name,
                self.badge_stack_max,
                self.crumbs,
                style=css.get("main").get("property"),
            )
        )
    
    def compile_mobile_component(self) -> Component:
        return rx.mobile_only(
            rx.vstack(
                self.name,
                self.badge_stack_min,
                self.crumbs,
                style=css.get("main").get("property"),
            )
        )

    def build(self) -> Box:
        self.box.children = [
            self.compile_desktop_component(),
            self.compile_mobile_component(),
        ]
        return self.box

# Footer class
class Footer:
    def __init__(self) -> None:
        self.footer: rx.Hstack = rx.hstack(style=css.get("footer"))
        self.footer.children.append(
            rx.text(
                "Copyright 2023 airaldo.com",
                font_size="10px",
                font_weight="semibold",
            )
        )
    def build(self) -> Hstack:
        return self.footer

@rx.page(route="/")
def landing() -> rx.Component:
    header: object = Header().build()
    main: object = Main().build()
    footer: object = Footer().build()

    return rx.vstack(
        header,
        main,
        footer,
        _light={
            "background": "radial-gradient(circle, rgba(0,0,0,0.35) 1px, transparent 1px)",
        "background_size": "25px 25px",
        },
        background='radial-gradient(circle, rgba(255,255,255,0.20) 1px, transparent 1px)',
        background_size='25px 25px',
        style= dots,
    )

app = rx.App(style=css.get("app"))
app.compile()
