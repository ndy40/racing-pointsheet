import logo from '../assets/pointsheet.png';
import {
    NavigationMenu, NavigationMenuContent, NavigationMenuIndicator,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList, NavigationMenuTrigger, NavigationMenuViewport
} from "~/components/ui/navigation-menu";

export function Navigation() {
    return <nav className="flex justify-between rounded-b-2xl h-auto bg-gray-700">
        <div className="w-full sm:px-6 lg:px-5">
            <div className="flex h-16 justify-between">
                <div id="logo" className="flex items-center space-x-4">
                    <img src={logo} alt="Pointsheet logo" className="size-10 rounded-full"/>
                    <h1 className="text-lg text-gray-100">Team Name</h1>
                </div>
                <NavigationMenu>
                    <NavigationMenuList className="flex space-x-2">
                        <NavigationMenuItem>
                            <NavigationMenuLink href="/calendar" className="text-white hover:bg-transparent hover:bg-gray-500 hover:text-gray-100">Calendar</NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink href="/races" className="text-white hover:bg-transparent hover:bg-gray-500 hover:text-gray-100">Races</NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink href="/drivers" className="text-white hover:bg-transparent hover:bg-gray-500 hover:text-gray-100">Drivers</NavigationMenuLink>
                        </NavigationMenuItem>
                    </NavigationMenuList>
                    <NavigationMenuViewport/>
                </NavigationMenu>

            </div>
        </div>
    </nav>
}
