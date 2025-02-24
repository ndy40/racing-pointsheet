import {TabItem, Tabs} from "~/components/tabs";
import LastRaceCard from "~/components/last_race_card";
import SeriesSignUpCard from "~/containers/dashboard/signedon-series";
import DashboardTabs from "~/containers/dashboard/tabs";



export default function Dashboard() {
    return <>
        <div className="flex flex-col gap-4">
            <section id="race-cards">
                <div id="top-panel" className="flex justify-between px-2 mt-5 h-auto">
                    <div id="top-card" className="flex flex-col gap-4 justify-around md:flex-row">
                        <LastRaceCard/>
                        <SeriesSignUpCard/>
                    </div>
                </div>
            </section>
            <section id="upcoming-tabs" className="mt-4">
                <DashboardTabs/>
            </section>
        </div>
    </>
}