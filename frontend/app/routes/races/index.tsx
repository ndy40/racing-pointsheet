import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarTrigger
} from "~/components/ui/menubar";
import {MenubarArrow} from "@radix-ui/react-menubar";
import {Separator} from "~/components/ui/separator";
import {useState} from "react";


export default function Events() {
    const [open, setOpen] = useState('');

    return <>
        <section role="menu" className="p-2">
            <Menubar className="bg-white border-none shadow-none bg-none px-15 gap-2" onValueChange={setOpen}>
                <MenubarMenu value="series">
                    <MenubarTrigger className="border border-gray-500 px-4 hover:bg-gray-200">
                        Series
                        {
                            open === 'series' ? (<span className="material-icons-outlined">keyboard_arrow_down</span>):(<span className="material-icons-outlined">keyboard_arrow_right</span>)
                        }
                    </MenubarTrigger>
                    <MenubarContent>
                        <MenubarItem>New Series</MenubarItem>
                        <MenubarItem>View</MenubarItem>
                        <MenubarArrow/>
                    </MenubarContent>
                </MenubarMenu>
                <MenubarMenu value="events">
                    <MenubarTrigger className="border border-gray-500 px-4 hover:bg-gray-200">
                        Events
                        {
                            open === 'events' ? (<span className="material-icons-outlined">keyboard_arrow_down</span>):(<span className="material-icons-outlined">keyboard_arrow_right</span>)
                        }
                    </MenubarTrigger>
                    <MenubarContent>
                        <MenubarItem>New Event</MenubarItem>
                        <MenubarItem>View</MenubarItem>
                    </MenubarContent>
                </MenubarMenu>
            </Menubar>
            <Separator className="my-2"/>
        </section>
        <section id="dashboard">
            <p>Dashboard section with stats and list of ongoing series and Events. Will show Calendar widget</p>
        </section>
    </>;
}