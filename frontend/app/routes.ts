import {type RouteConfig, index, route, layout,} from "@react-router/dev/routes";

export default [
    index("routes/_index.tsx"),
    route("/login", "routes/login.tsx"),
    layout("./layouts/authenticated.tsx", [
        route("/dashboard", "routes/dashboard.tsx"),
        route("/races", "routes/races/index.tsx", [
            route("series", "routes/races/series.tsx"),
            route("events", "routes/races/events.tsx"),
        ]),
    ]),
] satisfies RouteConfig;
