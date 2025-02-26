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

    return (
        <div className="p-2">
            <Menubar className="bg-white border-none shadow-none bg-none px-15 gap-2" onValueChange={setOpen}>
                <MenubarMenu value="series">
                    <MenubarTrigger className="border border-gray-500 px-4 hover:bg-gray-200">
                        Series
                        {
                            open === 'series' ? (<span className="material-icons-outlined">keyboard_arrow_down</span>):(<span className="material-icons-outlined">keyboard_arrow_right</span>)
                        }
                    </MenubarTrigger>
                    <MenubarContent>
                        <MenubarItem>View</MenubarItem>
                        <MenubarItem>Create New</MenubarItem>
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
                        <MenubarItem>View</MenubarItem>
                        <MenubarItem>Create</MenubarItem>
                    </MenubarContent>
                </MenubarMenu>
            </Menubar>
            <Separator className="my-2"/>

        </div>
        )
}