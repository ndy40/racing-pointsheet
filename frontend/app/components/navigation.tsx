import logo from './pointsheet.png';

export function Navigation() {
    return <nav className="flex justify-between rounded-b-2xl h-auto bg-gray-700">
        <div className="w-full px-4 sm:px-6 lg:px-5">
            <div className="flex h-16 justify-between">
                <div id="logo" className="flex items-center space-x-4">
                    <img src={logo} alt="Pointsheet logo" className="size-10 rounded-full"/>
                    <h1 className="text-lg text-gray-100">Team Name</h1>
                </div>
                {/* Menu items starts here */}
                <div className="flex items-center">
                    <a href="#" className="px-2 text-base text-gray-100 hover:text-gray-400">Schedule</a>
                    <a href="#" className="px-2 text-base text-gray-100 hover:text-gray-400">Series</a>
                    <a href="#" className="px-2 text-base text-gray-100 hover:text-gray-400">Drivers</a>
                    <a href="#" className="px-2"><span className="material-icons-outlined text-gray-400">account_circle</span></a>
                </div>
            </div>
        </div>
    </nav>
}
