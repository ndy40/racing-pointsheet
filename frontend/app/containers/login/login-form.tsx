import {useState} from "react";
import {Form} from "react-router";


export default function LoginForm() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    return (
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                    <a href="#" className="flex items-center mb-6 text-2xl font-semibold">
                        <img className="w-16 h-16 mr-2" src="http://pointsheet-app.com/pointsheet.png"
                             alt="logo"/>
                        Pointsheet Racing
                    </a>
                    <div
                        className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                                Sign in to your account
                            </h1>
                            <Form className="space-y-4 md:space-y-6" method="post">
                                <div>
                                    <label htmlFor="username"
                                           className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                                        Username</label>
                                    <input type="username" name="username" id="email" value={username} onChange={(e) => setUsername(e.target.value)}
                                           className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                           placeholder="Gammer tag" required/>
                                </div>
                                <div>
                                    <label htmlFor="password"
                                           className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                                    <input type="password" name="password" id="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)}
                                           className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                           required/>
                                </div>
                                <div className="flex items-center justify-between">
                                    <a href="#"
                                       className="text-sm font-medium text-gray-400 hover:underline">Forgot
                                        password?</a>
                                </div>
                                <button type="submit"
                                        className="w-full text-white bg-cyan-900 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Sign
                                    in
                                </button>
                                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                                    Don’t have an account yet? <a href="#"
                                                                  className="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign
                                    up</a>
                                </p>
                            </Form>
                        </div>
                    </div>
                </div>
    )
}