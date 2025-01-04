

export function Navigation() {
    return <nav className="flex justify-between border-b-2 h-10">
        <div id="logo" className="hidden md:flex">
            <h1 className="text-xl">Team name & Logo</h1>
        </div>
        <div className="flex items-center">
            <a href="#" className="px-2 text-base text-gray-500 hover:text-gray-700 hover:underline">Schedule</a>
            <a href="#" className="px-2 text-base text-gray-500 hover:text-gray-700 hover:underline">Series</a>
            <a href="#" className="px-2 text-base text-gray-500 hover:text-gray-700 hover:underline">Drivers</a>
            <a href="#" className="px-2"><span className="material-icons-outlined">account_circle</span></a>
        </div>
        
    </nav>
}
