import {type Context, createContext, useContext} from "react";


interface AuthContextProps {
    token?: string,
    isAuthenticated?: boolean,
}


export const AuthContext: Context<AuthContextProps>  = createContext({});


export const AuthProvider = ({children}: React.PropsWithChildren) => {

    const data: AuthContextProps = {
        token: "1234567890", isAuthenticated: true,
    }

    return <AuthContext.Provider value={data}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
    return useContext(AuthContext)
}
