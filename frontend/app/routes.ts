import {type RouteConfig, index, route, layout,} from "@react-router/dev/routes";

export default [
    index("routes/_index.tsx"),
    route("/login", "routes/login.tsx"),
] satisfies RouteConfig;
