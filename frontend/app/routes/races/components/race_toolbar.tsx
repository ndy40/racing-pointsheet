import {Menubar, MenubarContent, MenubarItem, MenubarMenu, MenubarTrigger} from "~/components/ui/menubar";
import {Link} from "react-router";
import {MenubarArrow} from "@radix-ui/react-menubar";
import {Separator} from "~/components/ui/separator";
import {useState} from "react";


export default function RaceToolbar() {
    const [open, setOpen] = useState('');

    return <>
        <section role="menu" className="p-2">
            <Menubar className="bg-white border-none shadow-none bg-none px-4 gap-2" onValueChange={setOpen}>
                <MenubarMenu value="series">
                    <MenubarTrigger className="border border-gray-200 px-4 ">
                        Series
                        {
                            open === 'series' ? (<span className="material-icons-outlined">keyboard_arrow_down</span>):(<span className="material-icons-outlined">keyboard_arrow_right</span>)
                        }
                    </MenubarTrigger>
                    <MenubarContent>
                        <MenubarItem asChild={true} className="hover:cursor-pointer"><Link to="/races/series">View</Link></MenubarItem>
                        <MenubarItem asChild={true}><Link to="/races/series/new">New Series</Link></MenubarItem>
                        <MenubarArrow/>
                    </MenubarContent>
                </MenubarMenu>
                <MenubarMenu value="events">
                    <MenubarTrigger className="border border-gray-300 px-4 hover:bg-gray-500 hover:text-white">
                        Events
                        {
                            open === 'events' ? (<span className="material-icons-outlined">keyboard_arrow_down</span>):(<span className="material-icons-outlined">keyboard_arrow_right</span>)
                        }
                    </MenubarTrigger>
                    <MenubarContent>
                        <MenubarItem asChild={true}><Link to="/races/events">View Events</Link></MenubarItem>
                        <MenubarItem asChild={true}><Link to="/races/events/new">New Event</Link></MenubarItem>
                    </MenubarContent>
                </MenubarMenu>
            </Menubar>
            <Separator className="my-2"/>
        </section>
    </>
}