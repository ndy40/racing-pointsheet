import SeriesSignUpCard from "@/containers/dashboard/signedon-series";
import LastRaceCard from "@/containers/dashboard/last-race";
import {TabItem, Tabs} from "@/components/tabs";
import {LargeRaceCard} from "@/components/race_card";
import EventCard from "@/containers/dashboard/event-card";

export default function Home() {
  return <>
      <div id="top-panel" className="flex justify-between px-2 mt-5 h-auto mt-12">
          <div id="top-card" className="flex gap-4 justify-around">
              <LastRaceCard/>
              <SeriesSignUpCard/>
          </div>
      </div>
    <div id="content-area" className="mt-8">
        <Tabs>
            <TabItem label="upcoming" title="Upcoming">
                <div className="grid grid-cols-2 gap-2">
                    <EventCard/>
                    <EventCard/>
                    <EventCard/>
                    <EventCard/>
                    <EventCard/>
                    <EventCard/>
                    <EventCard/>
                    
                </div>
            </TabItem>
            <TabItem title="Available" label="available">
                <h1>Available races</h1>
            </TabItem>
            <TabItem title="Series Standing" label="series_standing">
                <h1>Series standing</h1>
            </TabItem>
        </Tabs>
    </div>
  </>;
        
};
