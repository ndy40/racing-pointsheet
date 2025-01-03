import {ReactElement} from "react";


interface Props {
    children: ReactElement,
}


export default function RaceCard({children}: Props) {

    return <div className={"shadow bg-lime-50 min-w-40 h-full px-6 p-2 hover:shadow-lg"}>
        { children }
    </div>

}
