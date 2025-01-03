import SeriesSignUpCard from "@/containers/dashboard/signedon-series";
import LastRaceCard from "@/containers/dashboard/last-race";
import {Tabs} from "@/components/tabs";

export default function Home() {
  return <>
      <div id="top-panel" className="flex justify-between px-2 mt-5 h-auto mt-12">
          <div id="top-card" className="flex gap-4 justify-around">
              <LastRaceCard/>
              <SeriesSignUpCard/>
          </div>
      </div>
    <div id="content-area" className="mt-8">
        <Tabs/>
    </div>
  </>;
        
};
