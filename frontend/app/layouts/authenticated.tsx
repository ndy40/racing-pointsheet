import {Meta, Outlet, Scripts, ScrollRestoration} from "react-router";
import {Navigation} from "~/components/navigation";


export default function Authenticated() {
    return <html lang="en">
    <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
    </head>
    <body>
    <div id="wrapper" className="container mx-auto h-screen max-w-[960px]">
        <main>
            <Navigation/>
            <Outlet />
        </main>
    </div>
    <ScrollRestoration />
    <Scripts />
    </body>
    </html>
}