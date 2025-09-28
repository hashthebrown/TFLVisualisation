from dash_bootstrap_components import NavbarSimple, NavItem, NavLink

"""
A simple navigation bar with three links to different pages.
"""
navbar = NavbarSimple(
    children=[
        NavItem(NavLink("Map", href="/")),
        NavItem(NavLink("Busiest/Quietest Stations", href="/chart")),
        NavItem(NavLink("Average Entries", href="/average")),
    ],
    brand="Tube Stats",
    brand_href="/",
    color="dark",
    dark=True,
)
