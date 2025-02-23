


export function RaceCard({children}: {children: ReactElement}) {

    return <div className={"shadow bg-lime-50 min-w-40 h-full px-6 p-2 hover:shadow-lg rounded-lg"}>
        { children }
    </div>
}


export function LargeRaceCard({children}: {children: ReactElement}) {
    return <div className="w-auto shadow rounded-2xl px-4 py-4 basis-1/2">
        { children }
    </div>
}
