import {type RouteConfig, index, route, layout,} from "@react-router/dev/routes";

export default [
    index("routes/_index.tsx"),
    route("/login", "routes/login.tsx"),
    layout("./layouts/authenticated.tsx", [
        route("/dashboard", "routes/dashboard.tsx"),
        // races route.
        layout("./layouts/races_layout.tsx", [
            route("/races", "routes/races/index.tsx", [
                index("routes/races/home.tsx"),
                route("series", "routes/races/series/index.tsx", [
                    index("routes/races/series/view.tsx"),
                    route("new", "routes/races/series/new_series.tsx"),
                ]),
                route("events", "routes/races/events/index.tsx", [
                    index("routes/races/events/view.tsx"),
                    route("new", "routes/races/events/new_event.tsx"),
                ]),
            ]),
        ]),

        //     drivers route
        route("/drivers", "routes/drivers/index.tsx", [
            index("routes/drivers/home.tsx"),
        ]),

        //  calendar path
        route("/calendar", "routes/calendar/index.tsx")

    ]),
] satisfies RouteConfig;
