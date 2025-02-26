import {Meta, Outlet, Scripts, ScrollRestoration} from "react-router";
import {Navigation} from "~/components/navigation";


export default function Authenticated() {
    return (
        <>
                    <Navigation/>
                    <Outlet />
        </>

    );
}