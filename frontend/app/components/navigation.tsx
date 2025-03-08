import logo from '../assets/pointsheet-thumbnail.png';
import {
    NavigationMenu, NavigationMenuContent, NavigationMenuIndicator,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList, NavigationMenuTrigger, NavigationMenuViewport
} from "~/components/ui/navigation-menu";
import {Link} from "react-router";

export function Navigation() {
    return <nav className="flex justify-between rounded-b-2xl h-auto bg-gray-700">
        <div className="w-full sm:px-6 lg:px-5">
            <div className="flex h-16 justify-between">
                <Link to="/" className="flex items-center space-x-2 h-16">
                    <img src="/static/pointsheet-thumbnail.png" alt="Pointsheet logo" className="size-10 rounded-full"/>
                    <h1 className="text-lg text-gray-100">Team Name</h1>
                </Link>
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
