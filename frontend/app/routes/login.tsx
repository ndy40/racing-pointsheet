import {LoginForm} from "~/containers/login";
import type {Route} from './+types/login';
import {authenticateUser} from '~/lib/auth';
import {redirect} from "react-router";
import {userCookies} from "~/cookies.server";


export async function loader({request}: Route.LoaderArgs) {
    const cookieHeader = request.headers.get("Cookie");

    if (!cookieHeader) {
        return { isAuthenticated: false };
    }

    const cookie =
        (await userCookies.parse(cookieHeader)) || {};

    return cookie?.token && redirect("/");
}


export async function action({request}: Route.ActionArgs){
    let formData = await request.formData()

    let username = String(formData.get("username"))
    let password = String(formData.get("password"))

    try {
        const token = await authenticateUser(username, password)
        const cookie = (await userCookies.parse(request.headers.get("Cookie")) || {})


        if (token !== undefined) {
            cookie.token = token;
        }

        return redirect("/", {
            headers: {
                'Set-Cookie': await userCookies.serialize(cookie),
            }
        });
    } catch (e) {
        console.log("Error " + e)
    }
}

export default function Login({actionData}:Route.ComponentProps) {
    return (
        <section className="bg-gray-50">
                <LoginForm />
        </section>
    );
}