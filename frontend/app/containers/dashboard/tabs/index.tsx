import {Tabs, TabsContent, TabsList, TabsTrigger} from "~/components/ui/tabs";
import UpcomingEvents from "~/containers/dashboard/tabs/_upcoming";
import AvailableEvents from "~/containers/dashboard/tabs/_available_events";
import SeriesStanding from "~/containers/dashboard/tabs/_series_standing";


export default function DashboardTabs() {
    return <>
        <Tabs defaultValue="upcoming">
            <TabsList className="grid w-full grid-cols-3 gap-4">
                <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
                <TabsTrigger value="available">Available</TabsTrigger>
                <TabsTrigger value="standings">Series Standings</TabsTrigger>
            </TabsList>
            <TabsContent value="upcoming" className="px-4">
                <UpcomingEvents/>
            </TabsContent>
            <TabsContent value="available" className="px-4">
                <AvailableEvents/>
            </TabsContent>
            <TabsContent value="standings" className="px-4">
                <SeriesStanding/>
            </TabsContent>

        </Tabs>
    </>
}