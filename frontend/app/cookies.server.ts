import {createCookie} from "react-router";


export const userCookies = createCookie('user-auth', {
    path: '/',
    sameSite: 'lax',
    httpOnly: false,
    maxAge: 60,
    secure: false,

})