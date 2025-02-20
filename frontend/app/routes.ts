import {type RouteConfig, index, route,} from "@react-router/dev/routes";
import { flatRoutes } from '@react-router/fs-routes';

export default [
    // route("/" ,"routes/_index.tsx"),
    ...(await flatRoutes()),

] satisfies RouteConfig;
